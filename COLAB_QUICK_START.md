# 🚀 Entrenar en Google Colab (RECOMENDADO)

**Tiempo total: ~2 horas** con GPU gratis ⚡

---

## **¿POR QUÉ COLAB?**

✅ **GPU gratis** (Tesla T4 / A100)
✅ **10x más rápido** que tu computadora
✅ **Todo preinstalado** (PyTorch, CUDA, librerías)
✅ **No interfiere** con tu máquina
✅ **Fácil de usar** (solo hacer click)

---

## **PASOS (super simple)**

### **1️⃣ Abre Colab**

Haz clic aquí directamente (se abrirá un nuevo notebook):
```
https://colab.research.google.com/github/nick2331/Electiva_3/blob/claude/analyze-project-tech-oKyKr/VehiclEye_Training_Colab.ipynb
```

O manualmente:
1. Ve a https://colab.research.google.com/
2. Click **"Archivo"** → **"Abrir notebook"**
3. Pestaña **"GitHub"**
4. Ingresa: `nick2331/Electiva_3`
5. Selecciona: `VehiclEye_Training_Colab.ipynb`

---

### **2️⃣ Asegúrate de tener GPU**

En Colab: **Runtime** → **Change runtime type** → Selecciona:
```
Runtime type: Python 3
Hardware accelerator: GPU (T4 o mejor)
```
Click **Save**

---

### **3️⃣ Ejecuta las celdas en orden**

```
CELDA 1  → Verificar GPU
    ↓
CELDA 2  → Instalar dependencias (1 min)
    ↓
CELDA 3  → Clonar repo
    ↓
CELDA 4  → Descargar imágenes (15 min)
    ↓
CELDA 5  → ENTRENAR (1 hora 30 min)
           ☕ Tómate un café aquí
    ↓
CELDA 6  → Evaluar (2 min, opcional)
    ↓
CELDA 7  → Exportar a ONNX (1 min)
    ↓
CELDA 8  → Descargar modelo (2 min)
    ↓
CELDA 9  → Pasos siguientes
```

**Cómo ejecutar:** 
- Click en la celda
- Press **Shift + Enter** (o click el botón ▶️ a la izquierda)
- Espera a que termine (verás ✓ cuando listo)

---

### **4️⃣ Cuando termine CELDA 8**

Te descargarás automáticamente el archivo:
```
vehicleye.onnx (48 MB)
```

Debería estar en tu carpeta **"Descargas"**.

---

## **5️⃣ Subir a GitHub y Render**

### **A. Crear Release en GitHub:**

1. Ve a: https://github.com/nick2331/Electiva_3/releases
2. Click **"Create a new release"**
3. Rellena así:

```
Tag:       v1.0
Title:     Model v1.0 — EfficientNet-B0
Files:     vehicleye.onnx (el que descargaste de Colab)
```

4. Click **"Publish release"**

### **B. Copiar URL de descarga:**

En la release, **clic derecho** en `vehicleye.onnx`:
```
Copy link address
```

Te da algo como:
```
https://github.com/nick2331/Electiva_3/releases/download/v1.0/vehicleye.onnx
```

### **C. Configurar en Render:**

1. https://dashboard.render.com
2. Servicio: **vehicleye-api**
3. Pestaña: **Environment**
4. **Add Environment Variable:**

```
Key:   MODEL_DOWNLOAD_URL
Value: https://github.com/nick2331/Electiva_3/releases/download/v1.0/vehicleye.onnx
```

5. **Save** → Render redeploya automáticamente

---

### **6️⃣ Verificar que funcione**

Ve a tu panel admin (con contraseña):
```
https://vehicleye-api.onrender.com/api/v1/admin/health?admin_key=vehicleye-admin-2026
```

Busca la sección `"model"`. Debe decir:
```json
{
  "status": "ok",
  "message": "Modelo ONNX cargado en memoria"
}
```

✅ **Si dice "ok" = ¡FUNCIONANDO!**

---

### **7️⃣ Prueba en tu app**

1. Ve a: https://vehicleye.onrender.com/
2. Sube foto de un **Ford Raptor**
3. Espera respuesta...

**Antes:** "Hyundai Tucson 43%" (random) ❌
**Ahora:** "Ford Raptor 87%" (real) ✅

---

## **⏱️ CRONOGRAMA EXACTO**

| Celda | Qué hace | Tiempo | Notas |
|-------|----------|--------|-------|
| 1 | Verificar GPU | 30s | Debe decir "GPU: Tesla T4" |
| 2 | Instalar deps | 1 min | Espera a ver ✓ |
| 3 | Clonar repo | 1 min | Rápido |
| 4 | Descargar imágenes | 15 min | 1000+ imágenes, puede tardar |
| 5 | **ENTRENAR** | **90 min** | ☕ **Aquí esperas lo más** |
| 6 | Evaluar (opt) | 2 min | Muestra accuracy |
| 7 | Exportar ONNX | 1 min | Comprime PyTorch a ONNX |
| 8 | Descargar | 1 min | Descarga vehicleye.onnx |
| 9 | Instrucciones | 1 min | Lee pasos finales |
| **TOTAL** | | **~2 horas** | **Duración real** |

---

## **🆘 SI ALGO FALLA**

### **Error: "No GPU available"**
```
Solución: Runtime → Change runtime type → GPU
```

### **Error en CELDA 4 (descarga de imágenes)**
```
Solución: Es normal si Bing bloquea. El código hace fallback manual.
          Las imágenes que descargue son suficientes para entrenar.
```

### **CELDA 5 dice "CUDA out of memory"**
```
Solución: Reduce batch size. En ml/train.py línea 110:
          batch_size=32 → batch_size=16
```

### **No se descargó vehicleye.onnx en CELDA 8**
```
Solución: Descargalo manualmente:
          1. En Colab, click ≡ (menú) → Files
          2. Busca: ml/checkpoints/vehicleye.onnx
          3. Click derecho → Download
```

---

## **💡 NOTAS IMPORTANTES**

- **No necesitas instalar nada en tu PC** (solo descargar el .onnx)
- **Colab es completamente gratis** (con GPU T4)
- **El notebook se reinicia cada 12 horas**, pero el código guarda en Drive
- **Si algo se congela**, actualiza la página y continúa desde la celda siguiente

---

## **📚 SI QUIERES PERSONALIZAR**

En CELDA 5, puedes cambiar parámetros:

```python
!python ml/train.py \
  --data_dir ml/data/vehicleye_dataset \
  --epochs_phase1 5   # ← Cambiar aquí (menos = más rápido, peor accuracy) \
  --epochs_phase2 10  # ← Cambiar aquí (más = mejor, pero más lento) \
  --output ml/checkpoints/efficientnet_b0_vehicleye.pth
```

**Recomendado:** 5 + 10 = 15 épocas totales (buen balance)

---

## **✨ ¡LISTO!**

Simplemente:
1. Abre el link de Colab
2. Ejecuta las 9 celdas
3. Descarga vehicleye.onnx
4. Sube a GitHub
5. Configura en Render

**¡En 2 horas tendrás un modelo real clasificando vehículos!** 🚀

---

¿Dudas? Avísame cuando empieces. 💬
