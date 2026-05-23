"""
Clasificación de vehículos usando Groq Vision (Llama 4 Scout / Llama 3.2 Vision).

Flujo:
  1. Groq Vision analiza la imagen y devuelve marca/modelo del vehículo.
  2. El resultado se mapea a las 20 clases del catálogo colombiano.
  3. Groq Text genera una descripción enriquecida en español.

Si Groq falla (sin clave, timeout, error de red), retorna None
para que el llamador use el ONNX como respaldo.
"""
from __future__ import annotations

import base64
import json
import urllib.request
import urllib.error
from typing import NamedTuple

from app.config import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

VEHICLE_CLASSES: list[tuple[str, str]] = [
    ("Toyota", "Corolla"), ("Toyota", "Hilux"),
    ("Chevrolet", "Spark"), ("Chevrolet", "Aveo"),
    ("Renault", "Logan"), ("Renault", "Sandero"), ("Renault", "Stepway"),
    ("Mazda", "3"), ("Mazda", "CX-5"),
    ("Hyundai", "Tucson"), ("Hyundai", "Accent"),
    ("Kia", "Picanto"), ("Kia", "Rio"),
    ("Nissan", "Frontier"), ("Nissan", "Versa"),
    ("Ford", "Fiesta"), ("Ford", "Escape"),
    ("Volkswagen", "Gol"), ("Volkswagen", "Jetta"),
    ("Suzuki", "Swift"),
]

_CATALOG_STR = ", ".join(f"{b} {m}" for b, m in VEHICLE_CLASSES)


class GroqPrediction(NamedTuple):
    rank: int
    brand: str
    model: str
    confidence: float
    description: str


def _post_groq(payload: dict, timeout: int = 20) -> dict | None:
    key = settings.groq_api_key
    if not key:
        return None
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        GROQ_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="ignore")
        print(f"[Groq] HTTP {exc.code}: {body[:300]}")
        return None
    except Exception as exc:
        print(f"[Groq] Error: {exc}")
        return None


def _img_to_b64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode()


def classify_with_groq(image_bytes: bytes) -> list[GroqPrediction] | None:
    """
    Analiza la imagen con Groq Vision y devuelve top-3 predicciones.
    Retorna None si Groq no está configurado o falla.
    Retorna [] si el modelo decide que la imagen NO es un vehículo.
    """
    if not settings.groq_api_key:
        print("[Groq] GROQ_API_KEY no configurada.")
        return None

    print(f"[Groq] Clasificando con {settings.groq_vision_model}...")
    b64 = _img_to_b64(image_bytes)

    vision_prompt = f"""Eres un experto en identificación de vehículos del mercado colombiano.

Analiza la imagen y determina si contiene un vehículo automotor (carro, camioneta, SUV, pickup).

Si NO es un vehículo (persona, animal, objeto, paisaje, etc.), responde EXACTAMENTE:
{{"es_vehiculo": false}}

Si SÍ es un vehículo, identifica la marca y modelo más probable y responde EXACTAMENTE con este JSON (sin texto adicional):
{{
  "es_vehiculo": true,
  "predicciones": [
    {{"marca": "Toyota", "modelo": "Hilux", "confianza": 0.85, "descripcion": "camioneta pickup doble cabina"}},
    {{"marca": "Toyota", "modelo": "Corolla", "confianza": 0.08, "descripcion": "sedán compacto"}},
    {{"marca": "Nissan", "modelo": "Frontier", "confianza": 0.05, "descripcion": "pickup mediana"}}
  ]
}}

Catálogo disponible (prioriza estas marcas/modelos del mercado colombiano):
{_CATALOG_STR}

Si el vehículo que ves no está exactamente en el catálogo, elige el más similar.
Responde SOLO el JSON, nada más."""

    payload = {
        "model": settings.groq_vision_model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64}",
                        },
                    },
                    {"type": "text", "text": vision_prompt},
                ],
            }
        ],
        "temperature": 0.1,
        "max_tokens": 400,
    }

    resp = _post_groq(payload)
    if not resp:
        return None

    try:
        content = resp["choices"][0]["message"]["content"].strip()
        # Limpia posible markdown ```json ... ```
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        data = json.loads(content)
    except Exception as exc:
        print(f"[Groq] Error parseando respuesta: {exc}\nRespuesta: {resp}")
        return None

    if not data.get("es_vehiculo", True):
        return []  # señal explícita: no es vehículo

    preds_raw = data.get("predicciones", [])
    if not preds_raw:
        return None

    results: list[GroqPrediction] = []
    for i, p in enumerate(preds_raw[:3]):
        brand = p.get("marca", "").strip()
        model = p.get("modelo", "").strip()
        conf = float(p.get("confianza", 0.5))
        desc = p.get("descripcion", "")
        results.append(GroqPrediction(
            rank=i + 1,
            brand=brand,
            model=model,
            confidence=round(conf, 4),
            description=desc,
        ))

    return results if results else None


def generate_description(brand: str, model: str, confidence: float,
                          top3: list[tuple[str, str, float]]) -> str | None:
    """
    Genera una descripción automática rica en español usando Groq Text.
    Retorna None si Groq no está disponible.
    """
    if not settings.groq_api_key:
        return None

    top3_str = "\n".join(
        f"  {i+1}. {b} {m} ({c*100:.1f}%)" for i, (b, m, c) in enumerate(top3)
    )

    prompt = f"""Eres un asistente técnico de VehiclEye, un sistema de identificación de vehículos del mercado colombiano.

El sistema analizó una imagen y obtuvo los siguientes resultados:
- Predicción principal: {brand} {model} con {confidence*100:.1f}% de confianza
- Top 3 predicciones:
{top3_str}

Redacta UN SOLO párrafo en español (máximo 3 oraciones) que:
1. Mencione el vehículo identificado con su confianza
2. Describa brevemente ese vehículo (tipo de carrocería, uso típico en Colombia)
3. Si la confianza es menor al 60%, recomiende revisar las alternativas del top-3

No uses listas ni bullet points. Solo el párrafo. Sin saludos ni despedidas."""

    payload = {
        "model": settings.groq_text_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 200,
    }

    resp = _post_groq(payload)
    if not resp:
        return None

    try:
        return resp["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
