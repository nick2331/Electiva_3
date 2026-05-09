"""
Inferencia EfficientNet-B0.

Al arrancar el servidor se carga el modelo una sola vez en memoria.
Si el checkpoint no existe todavía (antes del primer entrenamiento),
se usan los pesos ImageNet con cabeza lineal aleatoria, lo que permite
probar el pipeline completo sin bloquear el arranque.
"""
from __future__ import annotations

import io
from pathlib import Path
from typing import NamedTuple

import torch
import timm
from PIL import Image
from torchvision import transforms

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

_PREPROCESS = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

_model: torch.nn.Module | None = None


class Prediction(NamedTuple):
    rank: int
    brand: str
    model: str
    confidence: float


def _build_model() -> torch.nn.Module:
    net = timm.create_model("efficientnet_b0", pretrained=False, num_classes=NUM_CLASSES)
    ckpt = Path(settings.model_path)
    if ckpt.exists():
        state = torch.load(ckpt, map_location="cpu", weights_only=True)
        net.load_state_dict(state)
    else:
        # Sin checkpoint — pretrained backbone, cabeza aleatoria para demo
        net = timm.create_model("efficientnet_b0", pretrained=True, num_classes=NUM_CLASSES)
    net.eval()
    return net


def get_model() -> torch.nn.Module:
    global _model
    if _model is None:
        _model = _build_model()
    return _model


def predict_bytes(image_bytes: bytes) -> list[Prediction]:
    model = get_model()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = _PREPROCESS(img).unsqueeze(0)

    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0]

    top_vals, top_idx = torch.topk(probs, min(3, NUM_CLASSES))
    results: list[Prediction] = []
    for rank, (idx, val) in enumerate(zip(top_idx.tolist(), top_vals.tolist()), start=1):
        brand, model_name = VEHICLE_CLASSES[idx]
        results.append(Prediction(rank=rank, brand=brand, model=model_name, confidence=round(val, 4)))
    return results


def predict_pil(img: Image.Image) -> list[Prediction]:
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return predict_bytes(buf.getvalue())
