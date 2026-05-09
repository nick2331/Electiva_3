"""
Evaluación completa del modelo: genera matriz de confusión, precision/recall/F1
y curvas de pérdida. Guarda el reporte en reports/model_metrics.pdf o .txt.

Uso:
  python ml/evaluate.py --data_dir ml/data/vehicleye_dataset --checkpoint ml/checkpoints/efficientnet_b0_vehicleye.pth
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

import timm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ml.dataset import VehiclEyeDataset, VEHICLE_CLASSES

NUM_CLASSES = len(VEHICLE_CLASSES)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASS_NAMES = [f"{b} {m}" for b, m in VEHICLE_CLASSES]


def load_model(checkpoint_path: str) -> torch.nn.Module:
    model = timm.create_model("efficientnet_b0", pretrained=False, num_classes=len(VEHICLE_CLASSES))
    state = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()
    return model.to(DEVICE)


@torch.no_grad()
def collect_predictions(model, loader):
    all_preds, all_labels = [], []
    for imgs, labels in loader:
        imgs = imgs.to(DEVICE)
        logits = model(imgs)
        preds = logits.argmax(dim=1).cpu().numpy()
        all_preds.extend(preds.tolist())
        all_labels.extend(labels.numpy().tolist())
    return np.array(all_labels), np.array(all_preds)


def plot_confusion_matrix(labels, preds, output_path: Path):
    cm = confusion_matrix(labels, preds)
    fig, ax = plt.subplots(figsize=(14, 12))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_NAMES)
    disp.plot(ax=ax, xticks_rotation=45, colorbar=False, cmap="Blues")
    ax.set_title("Matriz de confusión — VehiclEye EfficientNet-B0", fontsize=14)
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def save_report(labels, preds, cm_path: Path, output_path: Path):
    report = classification_report(labels, preds, target_names=CLASS_NAMES, digits=3)
    text = f"VehiclEye — Reporte de métricas\n{'='*60}\n\n{report}"

    try:
        from weasyprint import HTML

        html = f"""<html><body style='font-family:monospace;font-size:11px;padding:30px'>
        <h2>VehiclEye — Reporte de métricas del modelo</h2>
        <h3>EfficientNet-B0 con Transfer Learning</h3>
        <img src='{cm_path.resolve()}' style='max-width:100%;'>
        <pre style='margin-top:20px'>{report}</pre>
        </body></html>"""
        HTML(string=html).write_pdf(str(output_path.with_suffix(".pdf")))
        print(f"Reporte PDF guardado en: {output_path.with_suffix('.pdf')}")
    except Exception:
        output_path.with_suffix(".txt").write_text(text, encoding="utf-8")
        print(f"Reporte TXT guardado en: {output_path.with_suffix('.txt')}")

    print(f"\n{report}")


def main(args):
    ds = VehiclEyeDataset(args.data_dir, split="val")
    loader = DataLoader(ds, batch_size=32, shuffle=False, num_workers=2)

    model = load_model(args.checkpoint)
    labels, preds = collect_predictions(model, loader)

    out_dir = Path("reports")
    out_dir.mkdir(exist_ok=True)
    cm_path = out_dir / "confusion_matrix.png"
    metrics_path = out_dir / "model_metrics"

    plot_confusion_matrix(labels, preds, cm_path)
    save_report(labels, preds, cm_path, metrics_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="ml/data/vehicleye_dataset")
    parser.add_argument("--checkpoint", default="ml/checkpoints/efficientnet_b0_vehicleye.pth")
    main(parser.parse_args())
