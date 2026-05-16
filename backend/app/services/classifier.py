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
    """Ruta al archivo ONNX del modelo (importable desde otros módulos)."""
    return Path(settings.model_path).with_suffix(".onnx")


def _maybe_download() -> None:
    dst = _onnx_path()
    if dst.exists():
        return

    # Busca el archivo en rutas locales conocidas (p.ej. backend/vehicleye.onnx)
    _here = Path(__file__).resolve().parent.parent.parent  # directorio backend/
    for candidate in [
        _here / "vehicleye.onnx",
        Path("vehicleye.onnx"),
    ]:
        if candidate.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(str(candidate), str(dst))
            print(f"Modelo ONNX copiado desde {candidate}.")
            return

    url = getattr(settings, "model_download_url", "")
    if not url:
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


def _detect_non_vehicle(image_bytes: bytes) -> bool:
    """
    Heurística rápida sin modelo entrenado:
      - Detecta caras humanas con Haar cascade (cv2). Si hay una cara
        relativamente grande (>= 8 % del lado más corto), asumimos que
        la imagen es de una persona, no de un vehículo.
      - Revisa también la cantidad de píxeles con tono de piel; si más
        del 18 % de la imagen es piel humana, probablemente no es un
        vehículo.
    Devuelve True si decide que NO es un vehículo.
    """
    try:
        import cv2
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_bgr is None:
            return False
        h, w = img_bgr.shape[:2]
        short_side = min(h, w)

        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(cascade_path)
        min_face = max(40, short_side // 12)
        faces = cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(min_face, min_face)
        )
        for (_, _, fw, fh) in faces:
            if max(fw, fh) >= short_side * 0.08:
                return True

        # Tono de piel en espacio YCrCb (rangos aceptados en literatura).
        ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
        skin_mask = cv2.inRange(ycrcb, (0, 133, 77), (255, 173, 127))
        skin_ratio = float(skin_mask.sum()) / (255.0 * h * w)
        if skin_ratio > 0.18:
            return True

        return False
    except Exception:
        return False


def _try_external_api(image_bytes: bytes) -> list[Prediction] | None:
    """
    Llama al proveedor externo (Hugging Face / ImageNet) si está configurado.
    Devuelve:
      * lista de Predictions (top-3) si la API clasificó algo
      * lista vacía []  si la API decidió que NO es un vehículo
      * None  si no está configurada o falló
    """
    try:
        from app.services.external_classifier import classify_external
        results = classify_external(image_bytes)
    except Exception as exc:
        print(f"API externa falló: {exc}")
        return None

    if results is None:
        return None
    if results == []:
        return []  # señal explícita: la API dijo "no es un vehículo"

    return [
        Prediction(rank=i + 1, brand=brand, model=model,
                   confidence=round(float(score), 4))
        for i, (brand, model, score) in enumerate(results[:3])
    ]


def predict_bytes(image_bytes: bytes) -> list[Prediction]:
    sess = get_session()

    # Filtro previo: descartar fotos de personas antes de clasificar.
    if _detect_non_vehicle(image_bytes):
        return []

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Si no hay modelo ONNX local, intenta API externa (Hugging Face).
    # Si la API tampoco está configurada, cae a predicciones demo.
    if sess is None:
        ext = _try_external_api(image_bytes)
        if ext is not None:
            return ext
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
