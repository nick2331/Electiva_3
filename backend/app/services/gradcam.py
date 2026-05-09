"""
Generación de mapas Grad-CAM sobre la última capa convolucional de EfficientNet-B0.
Usa pytorch-grad-cam para el cómputo y guarda el resultado como imagen PNG en disco.
"""
from __future__ import annotations

import io
import uuid
from pathlib import Path

import numpy as np
from PIL import Image
from torchvision import transforms

from app.config import settings
from app.services.classifier import get_model, VEHICLE_CLASSES, _PREPROCESS

_CAM_TRANSFORM = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def _get_target_layer():
    model = get_model()
    # Última capa convolucional de EfficientNet-B0 en timm
    return model.blocks[-1][-1].conv_pwl


def generate_gradcam(image_bytes: bytes, class_idx: int) -> str:
    """
    Genera el mapa Grad-CAM para la clase indicada y guarda la imagen superpuesta.
    Devuelve el nombre del archivo guardado en gradcam_dir.
    """
    try:
        from pytorch_grad_cam import GradCAM
        from pytorch_grad_cam.utils.image import show_cam_on_image
        from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
    except ImportError:
        return _fallback_gradcam(image_bytes)

    model = get_model()
    target_layer = [_get_target_layer()]

    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    rgb_array = np.array(pil_img).astype(np.float32) / 255.0

    tensor = _CAM_TRANSFORM(Image.open(io.BytesIO(image_bytes)).convert("RGB")).unsqueeze(0)

    with GradCAM(model=model, target_layers=target_layer) as cam:
        targets = [ClassifierOutputTarget(class_idx)]
        grayscale_cam = cam(input_tensor=tensor, targets=targets)[0]

    visualization = show_cam_on_image(rgb_array, grayscale_cam, use_rgb=True)
    out_img = Image.fromarray(visualization)

    filename = f"gradcam_{uuid.uuid4().hex}.png"
    out_path = Path(settings.gradcam_dir) / filename
    out_img.save(out_path, format="PNG")
    return filename


def _fallback_gradcam(image_bytes: bytes) -> str:
    """
    Si pytorch-grad-cam no está instalado, guarda la imagen original redimensionada
    como placeholder para que el endpoint no falle.
    """
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    filename = f"gradcam_{uuid.uuid4().hex}.png"
    out_path = Path(settings.gradcam_dir) / filename
    pil_img.save(out_path, format="PNG")
    return filename
