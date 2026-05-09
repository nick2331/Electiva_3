# VehiclEye

Sistema inteligente de identificación y análisis de modelos de vehículos mediante visión por computador.

**Universidad Cooperativa de Colombia — Electiva III: Deep Learning Aplicado**

---

## Stack

| Capa | Tecnología |
|---|---|
| Modelo | EfficientNet-B0 (timm) + Transfer Learning |
| Backend | FastAPI + Uvicorn + SQLAlchemy |
| Frontend | React 18 + TypeScript + Vite + TailwindCSS |
| Base de datos | SQLite (local) / PostgreSQL (Render) |
| Despliegue | Render (Web Service + Static Site + PostgreSQL) |

---

## Inicio rápido — Local

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API disponible en `http://localhost:8000`  
Documentación OpenAPI en `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App disponible en `http://localhost:5173`

---

## Entrenamiento del modelo

```bash
# 1. Preparar dataset (estructura: ml/data/vehicleye_dataset/<marca_modelo>/*.jpg)
python ml/dataset.py --data_dir ml/data/vehicleye_dataset

# 2. Entrenar
python ml/train.py \
  --data_dir ml/data/vehicleye_dataset \
  --epochs_phase1 5 \
  --epochs_phase2 10 \
  --output ml/checkpoints/efficientnet_b0_vehicleye.pth

# 3. Evaluar (genera reports/model_metrics.pdf)
python ml/evaluate.py \
  --data_dir ml/data/vehicleye_dataset \
  --checkpoint ml/checkpoints/efficientnet_b0_vehicleye.pth
```

---

## Estructura del proyecto

```
vehicleye/
├── backend/          # FastAPI + servicios de IA
├── frontend/         # React + TypeScript
├── ml/               # Scripts de entrenamiento y evaluación
├── docs/             # Informe integrador PDF/DOCX
├── render.yaml       # Configuración de despliegue en Render
└── README.md
```

---

## Variables de entorno (backend)

| Variable | Default | Descripción |
|---|---|---|
| `DATABASE_URL` | sqlite+aiosqlite:///./vehicleye.db | URL de la base de datos |
| `MODEL_PATH` | ml/checkpoints/efficientnet_b0_vehicleye.pth | Checkpoint del modelo |
| `ADMIN_KEY` | vehicleye-admin-2026 | Clave del panel admin |
| `CONFIDENCE_THRESHOLD` | 0.15 | Umbral mínimo de confianza |

---

## Autores

- Nicolás Rubiano Giraldo — Gerente del Proyecto + Backend / IA
- Jeison Steven Ávila Soler — Frontend / UX
