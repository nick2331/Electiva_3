"""
Procesamiento de video: extrae un frame por segundo con OpenCV,
clasifica cada uno y consolida por promedio ponderado de confianza.
"""
from __future__ import annotations

import io
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from app.services.classifier import Prediction, predict_pil, NUM_CLASSES, VEHICLE_CLASSES
from app.config import settings

import torch
import timm
from torchvision import transforms


def _consolidate(frame_results: list[list[Prediction]]) -> list[Prediction]:
    """
    Promedia vectores de probabilidad ponderando por la confianza máxima del frame.
    Frames con confianza máxima baja contribuyen menos al resultado final.
    """
    if not frame_results:
        return []

    accum = np.zeros(NUM_CLASSES, dtype=np.float64)
    weight_sum = 0.0

    for preds in frame_results:
        vec = np.zeros(NUM_CLASSES, dtype=np.float64)
        for p in preds:
            idx = next(
                i for i, (b, m) in enumerate(VEHICLE_CLASSES)
                if b == p.brand and m == p.model
            )
            vec[idx] = p.confidence
        w = max(p.confidence for p in preds) if preds else 0.0
        accum += vec * w
        weight_sum += w

    if weight_sum == 0:
        return []

    avg = accum / weight_sum
    top3_idx = np.argsort(avg)[::-1][:3]
    results: list[Prediction] = []
    for rank, idx in enumerate(top3_idx, start=1):
        brand, model_name = VEHICLE_CLASSES[idx]
        results.append(Prediction(
            rank=rank,
            brand=brand,
            model=model_name,
            confidence=round(float(avg[idx]), 4),
        ))
    return results


def process_video(video_bytes: bytes) -> tuple[list[Prediction], Image.Image | None]:
    """
    Procesa un video MP4 y devuelve las predicciones consolidadas y el primer frame
    estable para usar como miniatura y Grad-CAM.
    """
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    cap = cv2.VideoCapture(tmp_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_interval = max(1, int(fps))
    max_frames = int(fps * settings.max_video_seconds)

    frame_results: list[list[Prediction]] = []
    thumbnail: Image.Image | None = None
    frame_count = 0
    extracted = 0

    while cap.isOpened() and frame_count <= max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb)
            preds = predict_pil(pil_img)
            frame_results.append(preds)
            if thumbnail is None and preds and preds[0].confidence > 0.3:
                thumbnail = pil_img
            extracted += 1
        frame_count += 1

    cap.release()
    Path(tmp_path).unlink(missing_ok=True)

    consolidated = _consolidate(frame_results)
    return consolidated, thumbnail
