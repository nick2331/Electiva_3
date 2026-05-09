"""
Generación de mapas de activación.
Con ONNX Runtime no hay autograd, así que se usa un mapa de calor
basado en la imagen original como placeholder visual hasta tener el modelo ONNX.
Cuando el modelo ONNX real esté disponible se puede integrar una implementación
de Grad-CAM compatible con onnxruntime (e.g. via onnx-interpretability).
"""
from __future__ import annotations

import io
import uuid
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from app.config import settings


def generate_gradcam(image_bytes: bytes, class_idx: int) -> str:
    """
    Genera un mapa visual de activación y lo guarda como PNG.
    Devuelve el nombre del archivo guardado.
    """
    try:
        return _saliency_map(image_bytes)
    except Exception:
        return _save_original(image_bytes)


def _saliency_map(image_bytes: bytes) -> str:
    """
    Pseudo Grad-CAM: resalta zonas de alta frecuencia (bordes y texturas)
    que son las regiones más informativas para un clasificador CNN.
    """
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    arr = np.array(pil_img, dtype=np.float32)

    # Mapa de bordes como proxy de zonas relevantes
    gray = np.mean(arr, axis=2)
    blurred = np.array(pil_img.filter(ImageFilter.GaussianBlur(radius=4)), dtype=np.float32).mean(axis=2)
    edge_map = np.abs(gray - blurred)
    edge_map = (edge_map - edge_map.min()) / (edge_map.max() - edge_map.min() + 1e-8)

    # Colormap jet manual (azul → verde → rojo)
    heatmap = np.zeros((224, 224, 3), dtype=np.uint8)
    heatmap[..., 0] = (np.clip(edge_map * 2 - 1, 0, 1) * 255).astype(np.uint8)   # R
    heatmap[..., 1] = (np.clip(1 - np.abs(edge_map * 2 - 1), 0, 1) * 255).astype(np.uint8)  # G
    heatmap[..., 2] = (np.clip(1 - edge_map * 2, 0, 1) * 255).astype(np.uint8)   # B

    overlay = (arr * 0.55 + heatmap * 0.45).clip(0, 255).astype(np.uint8)
    out_img = Image.fromarray(overlay)

    filename = f"gradcam_{uuid.uuid4().hex}.png"
    out_path = Path(settings.gradcam_dir) / filename
    out_img.save(out_path, format="PNG")
    return filename


def _save_original(image_bytes: bytes) -> str:
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    filename = f"gradcam_{uuid.uuid4().hex}.png"
    out_path = Path(settings.gradcam_dir) / filename
    pil_img.save(out_path, format="PNG")
    return filename
