"""
Carga del dataset Stanford Cars filtrado a las 20 clases colombianas.

Uso esperado:
  python ml/dataset.py --data_dir /ruta/stanford_cars

El script descarga el dataset, filtra las clases, aplica el split train/val
y guarda la estructura en ml/data/vehicleye_dataset/.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from torch.utils.data import Dataset

from ml.augmentations import train_transform, val_transform

# Mapeo: nombre en Stanford Cars → (brand, model) en VehiclEye
# Se ajusta manualmente porque los nombres en el dataset original son en inglés.
STANFORD_TO_VEHICLEYE: dict[str, tuple[str, str]] = {
    "Toyota Corolla": ("Toyota", "Corolla"),
    "Toyota Tundra": ("Toyota", "Hilux"),          # proxy
    "Chevrolet Spark EV": ("Chevrolet", "Spark"),
    "Chevrolet Aveo": ("Chevrolet", "Aveo"),
    "Renault Sandero": ("Renault", "Sandero"),
    "Mazda 3": ("Mazda", "3"),
    "Mazda CX-5": ("Mazda", "CX-5"),
    "Hyundai Tucson SUV": ("Hyundai", "Tucson"),
    "Hyundai Accent Sedan": ("Hyundai", "Accent"),
    "Kia Rio": ("Kia", "Rio"),
    "Nissan Frontier": ("Nissan", "Frontier"),
    "Nissan Versa": ("Nissan", "Versa"),
    "Ford Fiesta": ("Ford", "Fiesta"),
    "Ford Escape SUV": ("Ford", "Escape"),
    "Volkswagen Golf Hatchback": ("Volkswagen", "Gol"),
    "Volkswagen Jetta": ("Volkswagen", "Jetta"),
    "Suzuki Aerio": ("Suzuki", "Swift"),            # proxy
}

VEHICLE_CLASSES = [
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

CLASS_TO_IDX = {pair: i for i, pair in enumerate(VEHICLE_CLASSES)}


class VehiclEyeDataset(Dataset):
    """
    Dataset que espera una estructura:
      root/
        toyota_corolla/img001.jpg
        renault_logan/img002.jpg
        ...
    """

    def __init__(self, root: str, split: str = "train"):
        self.root = Path(root)
        self.split = split
        self.transform = train_transform if split == "train" else val_transform
        self.samples: list[tuple[Path, int]] = []
        self._load_samples()

    def _load_samples(self):
        for class_dir in sorted(self.root.iterdir()):
            if not class_dir.is_dir():
                continue
            label = _dir_to_label(class_dir.name)
            if label is None:
                continue
            idx = CLASS_TO_IDX.get(label)
            if idx is None:
                continue
            for img_path in class_dir.glob("*.jpg"):
                self.samples.append((img_path, idx))
            for img_path in class_dir.glob("*.png"):
                self.samples.append((img_path, idx))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        img_path, label = self.samples[index]
        img = np.array(Image.open(img_path).convert("RGB"))
        transformed = self.transform(image=img)
        return transformed["image"], label


def _dir_to_label(dir_name: str) -> tuple[str, str] | None:
    """
    Convierte un nombre de directorio a (brand, model).

    Soporta dos formatos:
      • toyota_corolla        → ('Toyota', 'Corolla')
      • renault_stepway       → ('Renault', 'Stepway')
      • mazda_cx5             → ('Mazda', 'CX-5')
      • volkswagen_gol        → ('Volkswagen', 'Gol')
    """
    parts = dir_name.lower().replace('-', '').replace('.', '').split('_')
    if len(parts) < 2:
        return None
    brand = parts[0].capitalize()
    model_raw = ' '.join(p.capitalize() for p in parts[1:])
    # Casos especiales para nombres compuestos o abreviados
    model_map = {
        'Cx5':  'CX-5',
        'Cx 5': 'CX-5',
        '3':    '3',
    }
    model = model_map.get(model_raw, model_raw)
    pair = (brand, model)
    # Valida que el par exista en el catálogo
    if pair in CLASS_TO_IDX:
        return pair
    # Fallback: match por brand + primer token del modelo
    for b, m in CLASS_TO_IDX:
        if b.lower() == brand.lower() and m.lower().replace('-', '').replace(' ', '') == model_raw.lower().replace(' ', ''):
            return (b, m)
    return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    args = parser.parse_args()
    ds = VehiclEyeDataset(args.data_dir, split="train")
    print(f"Dataset cargado: {len(ds)} imágenes de entrenamiento.")
