"""
Clasificación de vehículos vía APIs públicas (sin necesidad de entrenar modelo).

Soporta dos backends configurables vía la variable de entorno EXTERNAL_API_PROVIDER:

  * "huggingface" → Hugging Face Inference API
      - Modelo principal: HUGGINGFACE_MODEL (default: dima806/car_models_image_detection)
      - Token gratuito en https://huggingface.co/settings/tokens
      - Variable: HUGGINGFACE_TOKEN

  * "imagenet"   → Hugging Face con microsoft/resnet-50 (ImageNet 1000 clases)
      - No requiere token. Detecta categorías genéricas
        (sports car, pickup, minivan, jeep, ambulance, taxi, etc.)
      - Útil como fallback público sin registro.

  * "none" / vacío → desactivado (usa el modelo ONNX local o demo).

Cuando el provider devuelve clases ImageNet, se mapean a marcas/modelos del
catálogo VehiclEye usando heurísticas (sports car → genérico, pickup → Toyota Hilux,
SUV → Mazda CX-5, etc.). Cuando devuelve directamente marca/modelo, se intenta
hacer un match difuso con VEHICLE_CLASSES.
"""
from __future__ import annotations

import urllib.request
import urllib.error
import json
from typing import Optional

from app.config import settings


# ──────────────────────────────────────────────
# Tabla de mapeo ImageNet → catálogo VehiclEye
# (idx_imagenet) → (brand, model)
# Basado en las 1000 clases estándar de ImageNet.
# ──────────────────────────────────────────────
_IMAGENET_VEHICLE_MAP: dict[str, tuple[str, str]] = {
    # Pick-ups y camionetas
    "pickup":            ("Toyota",     "Hilux"),
    "pickup truck":      ("Toyota",     "Hilux"),
    "tow truck":         ("Nissan",     "Frontier"),

    # SUVs
    "jeep":              ("Mazda",      "CX-5"),
    "minivan":           ("Hyundai",    "Tucson"),

    # Sedanes / coupés / sports
    "sports car":        ("Mazda",      "3"),
    "sport car":         ("Mazda",      "3"),
    "convertible":       ("Volkswagen", "Jetta"),
    "limousine":         ("Volkswagen", "Jetta"),
    "limo":              ("Volkswagen", "Jetta"),
    "racer":             ("Mazda",      "3"),
    "racing car":        ("Mazda",      "3"),
    "race car":          ("Mazda",      "3"),

    # Compactos / urbanos
    "cab":               ("Chevrolet",  "Spark"),
    "taxi":              ("Chevrolet",  "Spark"),
    "hatchback":         ("Chevrolet",  "Spark"),

    # Vehículos especiales
    "ambulance":         ("Ford",       "Escape"),
    "fire engine":       ("Nissan",     "Frontier"),
    "fire truck":        ("Nissan",     "Frontier"),
    "police van":        ("Hyundai",    "Tucson"),
    "school bus":        ("Volkswagen", "Gol"),

    # Genérico "car"
    "car wheel":         ("Toyota",     "Corolla"),
    "beach wagon":       ("Renault",    "Stepway"),
    "station wagon":     ("Renault",    "Stepway"),
}

# Etiquetas que indican que NO es un vehículo
_NON_VEHICLE_LABELS = {
    "person", "human", "people", "man", "woman", "boy", "girl", "child",
    "face", "portrait", "selfie", "dog", "cat", "animal", "bird", "fish",
    "food", "fruit", "plant", "tree", "flower", "building", "house",
    "indoor", "kitchen", "bedroom",
}


def _is_vehicle_class(label: str) -> bool:
    """Devuelve True si la etiqueta ImageNet representa un vehículo."""
    label_lower = label.lower()
    if any(nv in label_lower for nv in _NON_VEHICLE_LABELS):
        return False
    vehicle_keywords = (
        "car", "truck", "van", "jeep", "suv", "pickup", "sedan", "coupe",
        "hatchback", "wagon", "convertible", "vehicle", "automobile",
        "ambulance", "taxi", "limo", "racer", "racing", "police",
    )
    return any(kw in label_lower for kw in vehicle_keywords)


def _map_imagenet_label(label: str) -> Optional[tuple[str, str]]:
    """Mapea una etiqueta ImageNet a (brand, model) del catálogo VehiclEye."""
    label_lower = label.lower().strip()
    if label_lower in _IMAGENET_VEHICLE_MAP:
        return _IMAGENET_VEHICLE_MAP[label_lower]
    # Match difuso por substrings
    for key, value in _IMAGENET_VEHICLE_MAP.items():
        if key in label_lower or label_lower in key:
            return value
    return None


def _parse_brand_model(label: str) -> Optional[tuple[str, str]]:
    """
    Si la API devuelve "Hyundai Tucson 2020" o "Ford F-150 Raptor",
    extrae (brand, model). Caso de fallback cuando no es ImageNet.
    """
    parts = label.replace("_", " ").split()
    if len(parts) < 2:
        return None
    brand = parts[0].capitalize()
    model = " ".join(parts[1:3]).title()
    return (brand, model)


# ──────────────────────────────────────────────
# Cliente HTTP simple (urllib, sin dependencias extras)
# ──────────────────────────────────────────────

def _http_post_image(url: str, image_bytes: bytes, headers: dict) -> Optional[list]:
    """POST imagen como octet-stream y devuelve JSON parseado, o None si falla."""
    try:
        req = urllib.request.Request(url, data=image_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                return None
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        # Hugging Face devuelve 503 mientras carga el modelo (cold-start)
        if e.code == 503:
            print(f"Hugging Face cargando modelo (503). Reintentando más tarde…")
        else:
            print(f"HuggingFace API HTTP {e.code}: {e.reason}")
        return None
    except Exception as exc:
        print(f"Error llamando a la API externa: {exc}")
        return None


# ──────────────────────────────────────────────
# Provider: Hugging Face Inference API
# ──────────────────────────────────────────────

_HF_BASE = "https://api-inference.huggingface.co/models/"


def classify_huggingface(image_bytes: bytes) -> Optional[list[dict]]:
    """
    Llama al modelo configurado en HUGGINGFACE_MODEL.
    Devuelve lista de dicts: [{"label": "Hyundai Tucson", "score": 0.87}, ...]
    """
    token = getattr(settings, "huggingface_token", "")
    model = getattr(settings, "huggingface_model", "dima806/car_models_image_detection")
    if not token:
        return None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
    }
    url = f"{_HF_BASE}{model}"
    data = _http_post_image(url, image_bytes, headers)
    if not isinstance(data, list):
        return None
    return data


def classify_imagenet(image_bytes: bytes) -> Optional[list[dict]]:
    """
    Modelo ImageNet (microsoft/resnet-50). Detecta 1000 clases genéricas.
    Útil como fallback público.
    """
    token = getattr(settings, "huggingface_token", "")
    headers = {"Content-Type": "application/octet-stream"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{_HF_BASE}microsoft/resnet-50"
    data = _http_post_image(url, image_bytes, headers)
    if not isinstance(data, list):
        return None
    return data


# ──────────────────────────────────────────────
# API pública: clasifica una imagen vía proveedor externo
# ──────────────────────────────────────────────

def classify_external(image_bytes: bytes) -> Optional[list[tuple[str, str, float]]]:
    """
    Devuelve top-3 (brand, model, confidence) o None si la API no está
    configurada / falló.
    """
    provider = (getattr(settings, "external_api_provider", "") or "").lower()
    if provider not in ("huggingface", "imagenet"):
        return None

    raw = classify_huggingface(image_bytes) if provider == "huggingface" else classify_imagenet(image_bytes)
    if not raw:
        return None

    # Verificar primero: ¿la respuesta indica que NO es un vehículo?
    top_label = str(raw[0].get("label", "")).lower()
    if not _is_vehicle_class(top_label) and provider == "imagenet":
        # ResNet-50 retorna algo no-vehículo con alta confianza → no es un carro
        if float(raw[0].get("score", 0)) > 0.25:
            return []  # señala "no es vehículo"

    results: list[tuple[str, str, float]] = []
    for item in raw[:10]:
        label = str(item.get("label", ""))
        score = float(item.get("score", 0.0))
        if score < 0.005:
            continue

        # 1) Intenta parsear "Brand Model"
        bm = _parse_brand_model(label)
        # 2) Si no, mapea ImageNet → catálogo
        if bm is None:
            bm = _map_imagenet_label(label)
        if bm is None:
            continue

        results.append((bm[0], bm[1], score))
        if len(results) >= 3:
            break

    return results or None
