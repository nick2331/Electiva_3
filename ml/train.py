"""
Entrenamiento de EfficientNet-B0 con transfer learning en dos fases.

Fase 1 (5 épocas)  — Backbone congelado, solo entrena el clasificador.
Fase 2 (10 épocas) — Se descongelan los dos últimos bloques y se afina con lr reducida.

Uso:
  python ml/train.py --data_dir ml/data/vehicleye_dataset --epochs_phase1 5 --epochs_phase2 10
"""
from __future__ import annotations

import argparse
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

import timm
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

from ml.dataset import VehiclEyeDataset, VEHICLE_CLASSES

NUM_CLASSES = len(VEHICLE_CLASSES)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def build_model(num_classes: int) -> nn.Module:
    model = timm.create_model("efficientnet_b0", pretrained=True, num_classes=num_classes)
    return model.to(DEVICE)


def freeze_backbone(model: nn.Module):
    for name, param in model.named_parameters():
        if "classifier" not in name:
            param.requires_grad = False


def unfreeze_last_blocks(model: nn.Module, num_blocks: int = 2):
    for param in model.parameters():
        param.requires_grad = False
    # Desbloquea cabeza
    for param in model.classifier.parameters():
        param.requires_grad = True
    # Desbloquea últimos N bloques del backbone
    for block in model.blocks[-num_blocks:]:
        for param in block.parameters():
            param.requires_grad = True


def train_one_epoch(model, loader, optimizer, criterion, scheduler=None):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        logits = model(imgs)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * imgs.size(0)
        preds = logits.argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += imgs.size(0)
    if scheduler:
        scheduler.step()
    return total_loss / total, correct / total


@torch.no_grad()
def validate(model, loader, criterion):
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
        logits = model(imgs)
        loss = criterion(logits, labels)
        total_loss += loss.item() * imgs.size(0)
        preds = logits.argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += imgs.size(0)
    return total_loss / total, correct / total


def run_phase(model, train_loader, val_loader, epochs, lr, tag):
    optimizer = AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=lr, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    print(f"\n--- {tag} ---")
    for epoch in range(1, epochs + 1):
        tr_loss, tr_acc = train_one_epoch(model, train_loader, optimizer, criterion, scheduler)
        val_loss, val_acc = validate(model, val_loader, criterion)
        print(
            f"Época {epoch:>3}/{epochs}  "
            f"loss_train={tr_loss:.4f}  acc_train={tr_acc:.4f}  "
            f"loss_val={val_loss:.4f}  acc_val={val_acc:.4f}"
        )


def main(args):
    dataset = VehiclEyeDataset(args.data_dir, split="train")
    val_size = max(1, int(len(dataset) * 0.15))
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    # Val usa transform de validación
    val_ds.dataset.split = "val"

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=2, pin_memory=True)
    val_loader   = DataLoader(val_ds,   batch_size=32, shuffle=False, num_workers=2, pin_memory=True)

    model = build_model(NUM_CLASSES)

    # FASE 1 — Backbone congelado
    freeze_backbone(model)
    run_phase(model, train_loader, val_loader, args.epochs_phase1, lr=1e-3, tag="FASE 1 — Cabeza lineal")

    # FASE 2 — Descongelado parcial
    unfreeze_last_blocks(model, num_blocks=2)
    run_phase(model, train_loader, val_loader, args.epochs_phase2, lr=1e-4, tag="FASE 2 — Fine-tuning")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), out)
    print(f"\nModelo guardado en: {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="ml/data/vehicleye_dataset")
    parser.add_argument("--epochs_phase1", type=int, default=5)
    parser.add_argument("--epochs_phase2", type=int, default=10)
    parser.add_argument("--output", default="ml/checkpoints/efficientnet_b0_vehicleye.pth")
    main(parser.parse_args())
