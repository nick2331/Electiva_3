"""
Generación de reportes PDF con WeasyPrint.
Construye HTML enriquecido y lo convierte a PDF.
"""
from __future__ import annotations

import base64
import io
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import settings
from app.schemas.responses import PredictionItem


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Helvetica Neue', Arial, sans-serif; color: #333; background: #fff; }}
  .cover {{ background: #0B3D91; color: white; padding: 40px; }}
  .cover h1 {{ font-size: 32px; letter-spacing: 2px; }}
  .cover p {{ margin-top: 8px; font-size: 14px; opacity: 0.85; }}
  .section {{ padding: 30px 40px; }}
  .section h2 {{ font-size: 16px; color: #0B3D91; border-bottom: 2px solid #0B3D91;
                 padding-bottom: 4px; margin-bottom: 16px; }}
  .image-box {{ text-align: center; margin: 16px 0; }}
  .image-box img {{ max-width: 360px; border-radius: 8px; border: 1px solid #ddd; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #0B3D91; color: white; padding: 8px 12px; text-align: left; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #eee; }}
  tr:nth-child(even) td {{ background: #f5f7fb; }}
  .bar-bg {{ background: #e5e7eb; border-radius: 4px; height: 12px; }}
  .bar-fill {{ background: #0B3D91; border-radius: 4px; height: 12px; }}
  .desc {{ background: #f5f7fb; border-left: 4px solid #0B3D91; padding: 16px 20px;
           font-size: 13px; line-height: 1.7; border-radius: 0 4px 4px 0; }}
  .footer {{ background: #f5f7fb; padding: 20px 40px; font-size: 11px; color: #888;
             text-align: center; margin-top: 20px; }}
  .badge {{ display: inline-block; background: #0B3D91; color: white; padding: 2px 8px;
            border-radius: 10px; font-size: 11px; margin-left: 8px; }}
  .warn {{ color: #C0392B; font-weight: bold; }}
</style>
</head>
<body>
<div class="cover">
  <h1>VehiclEye</h1>
  <p>Reporte de análisis #{analysis_id_short}</p>
  <p>Fecha: {date_str}  ·  Tipo: {input_type_label}</p>
</div>

<div class="section">
  <h2>Imagen analizada</h2>
  <div class="image-box">
    {image_tag}
  </div>
</div>

<div class="section">
  <h2>Resultados del clasificador</h2>
  {no_vehicle_block}
  <table>
    <tr>
      <th>#</th><th>Marca</th><th>Modelo</th><th>Confianza</th><th>Barra</th>
    </tr>
    {prediction_rows}
  </table>
</div>

<div class="section">
  <h2>Descripción automática</h2>
  <div class="desc">{description_es}</div>
</div>

<div class="footer">
  VehiclEye  ·  Universidad Cooperativa de Colombia  ·  Electiva III — Deep Learning Aplicado
</div>
</body>
</html>"""


def _prediction_row(p: PredictionItem) -> str:
    pct = round(p.confidence * 100, 1)
    fill_w = int(p.confidence * 100)
    return (
        f"<tr><td>{p.rank}</td><td>{p.brand}</td><td>{p.model}</td>"
        f"<td><strong>{pct} %</strong></td>"
        f"<td><div class='bar-bg'><div class='bar-fill' style='width:{fill_w}%'></div></div></td></tr>"
    )


def generate_pdf(
    analysis_id: str,
    input_type: str,
    predictions: list[PredictionItem],
    description_es: str,
    no_vehicle: bool,
    thumbnail_b64: Optional[str] = None,
) -> str:
    """
    Genera el PDF y lo guarda en reports_dir. Devuelve el nombre del archivo.
    """
    try:
        from weasyprint import HTML
    except Exception:
        return _txt_fallback(analysis_id, predictions, description_es)

    image_tag = ""
    if thumbnail_b64:
        image_tag = f'<img src="data:image/jpeg;base64,{thumbnail_b64}" alt="Vehículo analizado" />'

    no_vehicle_block = ""
    if no_vehicle:
        no_vehicle_block = (
            '<p class="warn">⚠ No se detectó un vehículo con suficiente confianza.</p>'
        )

    rows = "".join(_prediction_row(p) for p in predictions) if predictions else (
        "<tr><td colspan='5'>Sin predicciones disponibles</td></tr>"
    )

    date_str = datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")
    input_label = "Imagen" if input_type == "image" else "Video"

    html_content = _HTML_TEMPLATE.format(
        analysis_id_short=analysis_id[:8].upper(),
        date_str=date_str,
        input_type_label=input_label,
        image_tag=image_tag,
        no_vehicle_block=no_vehicle_block,
        prediction_rows=rows,
        description_es=description_es,
    )

    filename = f"report_{analysis_id}.pdf"
    out_path = Path(settings.reports_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        HTML(string=html_content).write_pdf(str(out_path))
        return filename
    except Exception:
        return _txt_fallback(analysis_id, predictions, description_es)


def _txt_fallback(analysis_id: str, predictions: list[PredictionItem], description_es: str) -> str:
    """Si WeasyPrint no está disponible, genera un archivo de texto plano como placeholder."""
    filename = f"report_{analysis_id}.txt"
    out_path = Path(settings.reports_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"VehiclEye — Reporte {analysis_id}", "=" * 50]
    for p in predictions:
        lines.append(f"  #{p.rank}  {p.brand} {p.model}  —  {round(p.confidence*100,1)} %")
    lines += ["", description_es]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return filename
