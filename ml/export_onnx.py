"""
Exporta el checkpoint PyTorch a formato ONNX para producción en Render.

Uso:
  python ml/export_onnx.py \
    --checkpoint ml/checkpoints/efficientnet_b0_vehicleye.pth \
    --output     ml/checkpoints/vehicleye.onnx

Luego sube vehicleye.onnx a GitHub Releases y pega la URL en MODEL_DOWNLOAD_URL en Render.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import torch
import timm

NUM_CLASSES = 20


def export(checkpoint: str, output: str):
    model = timm.create_model("efficientnet_b0", pretrained=False, num_classes=NUM_CLASSES)
    state = torch.load(checkpoint, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()

    dummy = torch.randn(1, 3, 224, 224)
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    torch.onnx.export(
        model,
        dummy,
        output,
        input_names=["input"],
        output_names=["logits"],
        opset_version=18,
    )
    size_mb = Path(output).stat().st_size / 1024 / 1024
    print(f"Modelo exportado: {output}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="ml/checkpoints/efficientnet_b0_vehicleye.pth")
    parser.add_argument("--output", default="ml/checkpoints/vehicleye.onnx")
    args = parser.parse_args()
    export(args.checkpoint, args.output)
