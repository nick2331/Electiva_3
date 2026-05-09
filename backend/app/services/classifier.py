"""
Inferencia con ONNX Runtime (~50 MB RAM vs ~600 MB de PyTorch).
Compatible con el free tier de Render (512 MB).

Flujo:
  1. Si existe ml/checkpoints/vehicleye.onnx  →  inferencia real.
  2. Si MODEL_DOWNLOAD_URL está configurada  →  descarga el .onnx al arrancar.
  3. Sin modelo disponible  →  predicciones demo aleatorias para probar el pipeline.
"""
from __future__ import annotations

import io
import random
import urllib.request
from pathlib import Path
from typing import NamedTuple

import numpy as np
from PIL import Image

from app.config import settings

VEHICLE_CLASSES: list[tuple[str, str]] = [
    ("Toyota", "Corolla"),
    ("Toyota", "Hilux"),
    ("Chevrolet", "Spark"),
    ("Chevrolet", "Aveo"),
    ("Renault", "Logan"),
    ("Renault", "Sandero"),
    ("Renault", "Stepway"),
    ("Mazda", "3"),
    ("Mazda", "CX-5"),
    ("Hyundai", "Tucson"),
    ("Hyundai", "Accent"),
    ("Kia", "Picanto"),
    ("Kia", "Rio"),
    ("Nissan", "Frontier"),
    ("Nissan", "Versa"),
    ("Ford", "Fiesta"),
    ("Ford", "Escape"),
    ("Volkswagen", "Gol"),
    ("Volkswagen", "Jetta"),
    ("Suzuki", "Swift"),
]

NUM_CLASSES = len(VEHICLE_CLASSES)

_IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
_IMAGENET_STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)

_session = None  # onnxruntime.InferenceSession


class Prediction(NamedTuple):
    rank: int
    brand: str
    model: str
    confidence: float


# ──────────────────────────────────────────────
# Preprocesamiento
# ──────────────────────────────────────────────

def _preprocess(img: Image.Image) -> np.ndarray:
    img = img.convert("RGB").resize((224, 224), Image.BILINEAR)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = (arr - _IMAGENET_MEAN) / _IMAGENET_STD
    arr = arr.transpose(2, 0, 1)        # HWC → CHW
    return arr[np.newaxis, :]           # añade batch dim → (1, 3, 224, 224)


# ──────────────────────────────────────────────
# Carga del modelo ONNX
# ──────────────────────────────────────────────

def _onnx_path() -> Path:
    base = Path(settings.model_path)
    # Acepta tanto .pth (legado) como .onnx
    return base.with_suffix(".onnx")


def _maybe_download() -> None:
    url = getattr(settings, "model_download_url", "")
    if not url:
        return
    dst = _onnx_path()
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando modelo ONNX desde {url} …")
    try:
        urllib.request.urlretrieve(url, str(dst))
        print("Modelo descargado correctamente.")
    except Exception as exc:
        print(f"No se pudo descargar el modelo: {exc}. Usando predicciones demo.")


def _load_session():
    global _session
    _maybe_download()
    path = _onnx_path()
    if not path.exists():
        print("Modelo ONNX no encontrado. El sistema usará predicciones demo.")
        return
    try:
        import onnxruntime as ort
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 1
        opts.inter_op_num_threads = 1
        _session = ort.InferenceSession(str(path), sess_options=opts,
                                        providers=["CPUExecutionProvider"])
        print("Modelo ONNX cargado correctamente.")
    except Exception as exc:
        print(f"Error al cargar el modelo ONNX: {exc}. Usando predicciones demo.")


def get_session():
    global _session
    if _session is None:
        _load_session()
    return _session


# ──────────────────────────────────────────────
# Inferencia
# ──────────────────────────────────────────────

def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - x.max())
    return e / e.sum()


def _demo_predictions() -> list[Prediction]:
    """Predicciones aleatorias para demo cuando no hay modelo entrenado."""
    indices = random.sample(range(NUM_CLASSES), 3)
    raw = sorted(random.uniform(0.1, 0.9) for _ in range(3))[::-1]
    total = sum(raw)
    confs = [round(v / total, 4) for v in raw]
    return [
        Prediction(rank=i + 1, brand=VEHICLE_CLASSES[idx][0],
                   model=VEHICLE_CLASSES[idx][1], confidence=confs[i])
        for i, idx in enumerate(indices)
    ]


def predict_bytes(image_bytes: bytes) -> list[Prediction]:
    sess = get_session()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    if sess is None:
        return _demo_predictions()

    tensor = _preprocess(img)
    input_name = sess.get_inputs()[0].name
    logits = sess.run(None, {input_name: tensor})[0][0]
    probs = _softmax(logits)

    top3_idx = np.argsort(probs)[::-1][:3]
    return [
        Prediction(
            rank=rank,
            brand=VEHICLE_CLASSES[idx][0],
            model=VEHICLE_CLASSES[idx][1],
            confidence=round(float(probs[idx]), 4),
        )
        for rank, idx in enumerate(top3_idx, start=1)
    ]


def predict_pil(img: Image.Image) -> list[Prediction]:
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return predict_bytes(buf.getvalue())
