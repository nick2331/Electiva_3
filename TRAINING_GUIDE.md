# 🚗 GUÍA DE ENTRENAMIENTO - VehiclEye

**Importante:** El entrenamiento se hace en tu computadora local, NO en Render.

---

## **PASO 1: Instalar dependencias (5 minutos)**

Abre terminal en `/home/user/Electiva_3` y ejecuta:

```bash
# Instalar PyTorch (según tu SO)
# En Windows/macOS/Linux con CPU:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# En macOS con Apple Silicon:
pip install torch torchvision torchaudio

# Instalar dependencias de ML
pip install timm pillow bing-image-downloader requests

# Verificar instalación
python -c "import torch; print(f'✓ PyTorch {torch.__version__}')"
```

---

## **PASO 2: Descargar imágenes (10-30 minutos)**

```bash
cd /home/user/Electiva_3

# Opción A: Automático (requiere bing-image-downloader)
python ml/download_dataset.py --output ml/data/vehicleye_dataset --per_class 60

# Opción B: Manual (si A falla)
# 1. Ve a https://images.google.com/
# 2. Busca: "Toyota Corolla car" → descarga 60 imágenes
# 3. Crea carpeta: ml/data/vehicleye_dataset/Toyota/Corolla/
# 4. Mueve imágenes ahí
# 5. Repite para los 20 modelos
```

**Estructura esperada después:**
```
ml/data/vehicleye_dataset/
├── Toyota/
│   ├── Corolla/
│   │   ├── img_1.jpg
│   │   ├── img_2.jpg
│   │   └── ... (60 imágenes)
│   └── Hilux/
│       └── ... (60 imágenes)
├── Chevrolet/
│   ├── Spark/
│   └── Aveo/
└── ... (resto de marcas)
```

---

## **PASO 3: Entrenar el modelo (1-3 horas en CPU)**

```bash
cd /home/user/Electiva_3

# Entrenar con configuración por defecto (15 épocas)
python ml/train.py

# O con parámetros personalizados:
python ml/train.py \
  --data_dir ml/data/vehicleye_dataset \
  --epochs_phase1 5 \
  --epochs_phase2 10 \
  --output ml/checkpoints/efficientnet_b0_vehicleye.pth
```

**Salida esperada:**
```
--- FASE 1 — Cabeza lineal ---
Época   1/5  loss_train=2.456  acc_train=0.34  loss_val=2.123  acc_val=0.41
Época   2/5  loss_train=1.234  acc_train=0.67  loss_val=0.987  acc_val=0.72
...
Época   5/5  loss_train=0.456  acc_train=0.89  loss_val=0.512  acc_val=0.88

--- FASE 2 — Fine-tuning ---
Época   1/10 loss_train=0.123  acc_train=0.92  loss_val=0.145  acc_val=0.91
...
Época  10/10 loss_train=0.045  acc_train=0.97  loss_val=0.067  acc_val=0.96

Modelo guardado en: ml/checkpoints/efficientnet_b0_vehicleye.pth ✓
```

**Duración:**
- GPU (NVIDIA/Apple Silicon): 10-30 minutos
- CPU: 1-3 horas
- Si el RAM se agota, reduce batch_size en ml/train.py línea 110

---

## **PASO 4: Evaluar el modelo (2 minutos)**

```bash
python ml/evaluate.py
```

**Genera:**
- `reports/model_metrics.txt` → Accuracy, Precision, Recall por clase
- `reports/model_metrics.pdf` → Gráficos de confusión

---

## **PASO 5: Exportar a ONNX (1 minuto)**

ONNX es el formato que funciona en Render (sin PyTorch).

```bash
python ml/export_onnx.py \
  --checkpoint ml/checkpoints/efficientnet_b0_vehicleye.pth \
  --output ml/checkpoints/vehicleye.onnx
```

**Salida esperada:**
```
✓ Modelo exportado: ml/checkpoints/vehicleye.onnx (47.3 MB)
```

---

## **PASO 6: Subir a GitHub Releases (5 minutos)**

El archivo `vehicleye.onnx` es demasiado grande para git (~50 MB), así que se sube como Release.

### **6a. Crear Release en GitHub:**

```bash
cd /home/user/Electiva_3
git tag -a v1.0 -m "Modelo entrenado EfficientNet-B0"
git push origin v1.0
```

Ve a: https://github.com/nick2331/Electiva_3/releases

Click **"Create a new release"** → 
- Tag: `v1.0`
- Title: `Model v1.0 — EfficientNet-B0`
- Sube el archivo: `ml/checkpoints/vehicleye.onnx`
- Publish

### **6b. Copiar URL de descarga:**

En la release, haz clic derecho en `vehicleye.onnx` → "Copy link address":
```
https://github.com/nick2331/Electiva_3/releases/download/v1.0/vehicleye.onnx
```

---

## **PASO 7: Configurar en Render (2 minutos)**

En Render Dashboard → tu servicio `vehicleye-api` → **Environment** → agregar:

```
MODEL_DOWNLOAD_URL=https://github.com/nick2331/Electiva_3/releases/download/v1.0/vehicleye.onnx
```

Click **Save**.

Render redespliega automáticamente. Revisa en `logs` que descargó el modelo:
```
Descargando modelo ONNX desde https://github.com/...
Modelo descargado correctamente.
Modelo ONNX cargado correctamente.
```

Verifica en `/admin/health`:
```json
{
  "model": {
    "status": "ok",
    "message": "Modelo ONNX cargado en memoria"
  }
}
```

---

## **PASO 8: Probar (2 minutos)**

1. Ve a tu frontend en Render
2. Sube la foto de un Ford Raptor
3. ✅ Espera "Ford Raptor" o similar (no "random car")

---

## **SI ALGO FALLA**

### **Error: `No module named 'torch'`**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### **Error: `CUDA out of memory`**
La GPU no tiene suficiente RAM. Solución:
```bash
# Entrenar en CPU
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu

# O reduce batch_size en ml/train.py línea 110
# Cambiar: batch_size=32 → batch_size=16 o 8
```

### **Error: `No module named 'bing_image_downloader'`**
```bash
pip install bing-image-downloader
# O descarga manualmente de Google Images
```

### **El modelo es muy malo (~50% accuracy)**
Probablemente el dataset tiene imágenes de baja calidad o muy pocas.
- Aumenta a 100+ imágenes por clase
- Asegúrate que las imágenes sean carros (no logos, no planos)
- Varía ángulos, luces, colores

---

## **RESUMEN: COMANDOS FINALES (copiar y pegar)**

```bash
# 1. Instalar
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install timm pillow bing-image-downloader

# 2. Descargar dataset
cd /home/user/Electiva_3
python ml/download_dataset.py --per_class 60

# 3. Entrenar
python ml/train.py

# 4. Evaluar
python ml/evaluate.py

# 5. Exportar ONNX
python ml/export_onnx.py

# 6. Subir a GitHub (después de crear release manualmente)

# 7. Configurar MODEL_DOWNLOAD_URL en Render
# 8. Probar en frontend
```

¿Listo? ¡Empecemos! 🚀
