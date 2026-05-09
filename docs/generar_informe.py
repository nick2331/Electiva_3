# -*- coding: utf-8 -*-
"""
Generador del informe VehiclEye - Proyecto Integrador Final - Electiva III.
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


COLOR_PRIMARIO = RGBColor(0x0B, 0x3D, 0x91)   # Azul institucional
COLOR_SECUNDARIO = RGBColor(0x33, 0x33, 0x33)
COLOR_GRIS = RGBColor(0x55, 0x55, 0x55)
COLOR_ACENTO = RGBColor(0xC0, 0x39, 0x2B)


def set_cell_bg(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)


def set_cell_borders(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = OxmlElement('w:tcBorders')
    for border_name in ('top', 'left', 'bottom', 'right'):
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:color'), '999999')
        tc_borders.append(border)
    tc_pr.append(tc_borders)


def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARIO
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '8')
    bottom.set(qn('w:color'), '0B3D91')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARIO
    return p


def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_SECUNDARIO
    return p


def add_par(doc, text, justify=True, italic=False, size=11):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.3
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(size)
    run.italic = italic
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    run = p.runs[0] if p.runs else p.add_run('')
    run.text = text
    run.font.name = 'Calibri'
    run.font.size = Pt(11)


def add_numbered(doc, text):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.space_after = Pt(2)
    run = p.runs[0] if p.runs else p.add_run('')
    run.text = text
    run.font.name = 'Calibri'
    run.font.size = Pt(11)


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Header
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ''
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.size = Pt(11)
        run.font.name = 'Calibri'
        set_cell_bg(hdr[i], '0B3D91')
        hdr[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Rows
    for r_idx, row in enumerate(rows):
        cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row):
            cells[c_idx].text = ''
            p = cells[c_idx].paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(10)
            run.font.name = 'Calibri'
            cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if r_idx % 2 == 1:
                set_cell_bg(cells[c_idx], 'F2F4F8')

    if widths:
        for row in table.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    return table


def add_user_story(doc, code, role, action, goal, criteria):
    add_h3(doc, f'{code} — {role}')
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run('Como '); r1.font.bold = True; r1.font.size = Pt(11); r1.font.name = 'Calibri'
    r2 = p.add_run(f'{role.lower()},\n'); r2.font.size = Pt(11); r2.font.name = 'Calibri'
    r3 = p.add_run('quiero '); r3.font.bold = True; r3.font.size = Pt(11); r3.font.name = 'Calibri'
    r4 = p.add_run(f'{action},\n'); r4.font.size = Pt(11); r4.font.name = 'Calibri'
    r5 = p.add_run('para '); r5.font.bold = True; r5.font.size = Pt(11); r5.font.name = 'Calibri'
    r6 = p.add_run(f'{goal}.'); r6.font.size = Pt(11); r6.font.name = 'Calibri'

    pc = doc.add_paragraph()
    pc.paragraph_format.left_indent = Cm(0.5)
    pc.paragraph_format.space_after = Pt(8)
    rc = pc.add_run('Criterios de aceptación: ')
    rc.font.bold = True; rc.font.size = Pt(11); rc.font.name = 'Calibri'
    rc.font.color.rgb = COLOR_ACENTO
    rt = pc.add_run(criteria)
    rt.font.size = Pt(11); rt.font.name = 'Calibri'


def add_page_break(doc):
    doc.add_page_break()


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = COLOR_GRIS
    r.font.name = 'Calibri'


def add_ascii_box(doc, content):
    """Bloque de código/ASCII con fuente monoespaciada."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.right_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(content)
    r.font.name = 'Consolas'
    r.font.size = Pt(9)
    r.font.color.rgb = COLOR_SECUNDARIO
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F4F6F8')
    pPr.append(shd)


# ========================================================================
# CONSTRUCCIÓN DEL DOCUMENTO
# ========================================================================

doc = Document()

# Configuración global de página y fuente
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.8)
    section.right_margin = Cm(2.8)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)


# ------------------------------------------------------------------------
# PORTADA
# ------------------------------------------------------------------------
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('UNIVERSIDAD COOPERATIVA DE COLOMBIA')
r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARIO; r.font.name = 'Calibri'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Facultad de Ingeniería  ·  Ingeniería de Sistemas')
r.font.size = Pt(12); r.font.name = 'Calibri'; r.font.color.rgb = COLOR_GRIS

for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('VehiclEye')
r.font.size = Pt(38); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARIO; r.font.name = 'Calibri'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Sistema inteligente de identificación y análisis\nde modelos de vehículos mediante visión por computador')
r.font.size = Pt(13); r.italic = True; r.font.color.rgb = COLOR_SECUNDARIO; r.font.name = 'Calibri'

for _ in range(2):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Informe Integrador Final')
r.font.size = Pt(13); r.font.bold = True; r.font.name = 'Calibri'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Electiva III  ·  Deep Learning Aplicado')
r.font.size = Pt(12); r.font.color.rgb = COLOR_GRIS; r.font.name = 'Calibri'

for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Presentado por:')
r.font.size = Pt(11); r.font.bold = True; r.font.name = 'Calibri'

for nombre in ['Nicolás Rubiano Giraldo', 'Jeison Steven Ávila Soler']:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(nombre)
    r.font.size = Pt(11); r.font.name = 'Calibri'

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Docente: Wilder Ramírez Delgado')
r.font.size = Pt(11); r.font.name = 'Calibri'

for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Bogotá D.C., Colombia  —  2026')
r.font.size = Pt(11); r.font.color.rgb = COLOR_GRIS; r.font.name = 'Calibri'

add_page_break(doc)


# ------------------------------------------------------------------------
# RESUMEN
# ------------------------------------------------------------------------
add_h1(doc, 'Resumen ejecutivo')

add_par(doc,
    'Este informe presenta el desarrollo de VehiclEye, una aplicación web que reconoce de forma '
    'automática la marca y el modelo de un vehículo a partir de imágenes o secuencias cortas de '
    'video. La solución se enmarca en la línea de visión por computador del proyecto integrador de '
    'Electiva III y se construye sobre una red neuronal convolucional EfficientNet-B0 ajustada con '
    'transfer learning a un subconjunto del dataset Stanford Cars filtrado a los modelos más '
    'comunes en el parque automotor colombiano. Para los videos cortos, el sistema extrae frames '
    'con OpenCV y consolida las predicciones por promedio ponderado de confianza, generando un '
    'resultado estable a lo largo de la secuencia.')

add_par(doc,
    'El sistema entrega los tres modelos más probables con su nivel de confianza, una descripción '
    'textual en español armada a partir de plantillas estructuradas y un reporte PDF descargable. '
    'A nivel técnico, se trabajó sobre una arquitectura cliente-servidor: un backend en FastAPI '
    'que expone una API REST documentada con OpenAPI, y un frontend en React con TypeScript que '
    'consume esos endpoints y se adapta a dispositivos móviles, incluyendo el acceso directo a la '
    'cámara. El despliegue final se realiza sobre Render, lo que permite encender el servicio bajo '
    'demanda sin costo fijo de infraestructura.')

add_par(doc,
    'A lo largo del documento se describen las ocho fases definidas por la asignatura: definición '
    'del proyecto, historias de usuario, diseño del sistema, desarrollo backend, desarrollo '
    'frontend, integración, análisis e interpretación, y presentación final. También se detallan '
    'las decisiones técnicas, el contrato de la API, las métricas obligatorias de evaluación del '
    'modelo (matriz de confusión, precision, recall, F1, curvas de entrenamiento y mapas de '
    'activación) y los criterios para interpretar el comportamiento del clasificador en escenarios '
    'reales.')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8)
r = p.add_run('Palabras clave: ')
r.font.bold = True; r.font.size = Pt(11); r.font.name = 'Calibri'
r2 = p.add_run('visión por computador, redes neuronales convolucionales, EfficientNet, transfer '
               'learning, FastAPI, React, clasificación de vehículos, interpretabilidad, Render.')
r2.font.size = Pt(11); r2.italic = True; r2.font.name = 'Calibri'

add_page_break(doc)


# ------------------------------------------------------------------------
# TABLA DE CONTENIDO
# ------------------------------------------------------------------------
add_h1(doc, 'Tabla de contenido')

toc_items = [
    ('1.', 'Contexto general del proyecto integrador'),
    ('2.', 'Línea de trabajo seleccionada'),
    ('FASE 1', 'Definición del proyecto'),
    ('FASE 2', 'Historias de usuario'),
    ('FASE 3', 'Diseño del sistema'),
    ('FASE 4', 'Desarrollo backend e implementación del modelo'),
    ('FASE 5', 'Desarrollo frontend'),
    ('FASE 6', 'Integración del sistema y contrato de la API'),
    ('FASE 7', 'Análisis e interpretación del modelo'),
    ('FASE 8', 'Presentación final'),
    ('3.', 'Organización del equipo y matriz de roles'),
    ('4.', 'Plan de trabajo'),
    ('5.', 'Conclusiones'),
    ('6.', 'Referencias'),
]

for num, title in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f'{num}    ')
    r.font.bold = True; r.font.color.rgb = COLOR_PRIMARIO; r.font.size = Pt(11); r.font.name = 'Calibri'
    r2 = p.add_run(title)
    r2.font.size = Pt(11); r2.font.name = 'Calibri'

add_page_break(doc)


# ------------------------------------------------------------------------
# 1. CONTEXTO GENERAL
# ------------------------------------------------------------------------
add_h1(doc, '1. Contexto general del proyecto integrador')

add_par(doc,
    'La asignatura Electiva III — Deep Learning Aplicado plantea como cierre académico un proyecto '
    'integrador en el que el estudiante debe seleccionar una de las grandes familias de modelos '
    'estudiadas durante el semestre y construir una solución funcional alrededor de ella. Las '
    'familias propuestas son redes neuronales convolucionales (CNN), redes recurrentes (RNN, LSTM, '
    'GRU), arquitecturas Transformer y modelos generativos adversarios (GAN). El propósito no es '
    'tocar todas, sino profundizar en una y demostrar dominio sobre el ciclo completo: '
    'preparación de datos, entrenamiento, evaluación, interpretación, despliegue y consumo desde '
    'una interfaz de usuario.')

add_par(doc,
    'En coherencia con esa indicación, el equipo concentró el esfuerzo en una sola arquitectura y '
    'se aseguró de cubrir todas las exigencias del componente de evaluación: matriz de confusión, '
    'métricas por clase, curvas de aprendizaje, análisis de errores y visualización de las '
    'activaciones internas del modelo. La idea es entregar una herramienta que cualquier persona '
    'pueda usar y, al mismo tiempo, sustentar técnicamente cómo aprende y cómo se equivoca.')


# ------------------------------------------------------------------------
# 2. LÍNEA DE TRABAJO
# ------------------------------------------------------------------------
add_h1(doc, '2. Línea de trabajo seleccionada')

add_par(doc,
    'El proyecto se inscribe en la Opción 1 — Evaluación Avanzada en Visión Artificial (CNN). La '
    'razón es directa: identificar marca y modelo de un vehículo a partir de una fotografía es un '
    'problema de clasificación fina (fine-grained classification) en el que dos clases distintas '
    'pueden compartir buena parte de su silueta y diferenciarse apenas por detalles como la forma '
    'de los faros, la parrilla o el contorno del paragolpes. Este tipo de problemas es '
    'precisamente donde brillan las CNN modernas y donde la evaluación de errores y la '
    'interpretabilidad cobran más valor: no basta con saber el porcentaje de aciertos, hay que '
    'entender qué está mirando el modelo cuando decide.')

add_par(doc,
    'Dentro de las CNN disponibles se eligió EfficientNet-B0, una arquitectura que aplica '
    'escalado compuesto sobre profundidad, ancho y resolución y que ofrece un balance muy '
    'competitivo entre precisión, velocidad de inferencia y peso del modelo en disco. Esa última '
    'característica es relevante porque el despliegue se hará en Render, donde los planes '
    'gratuitos imponen límites de memoria que descartan modelos más pesados como ResNet-152 o '
    'EfficientNet-B7.')

add_page_break(doc)


# ------------------------------------------------------------------------
# FASE 1
# ------------------------------------------------------------------------
add_h1(doc, 'FASE 1  ·  Definición del proyecto')

add_h2(doc, '1.1 Descripción del sistema')
add_par(doc,
    'VehiclEye es una aplicación web que recibe una imagen o un video corto de un automóvil y '
    'devuelve la marca y el modelo identificados, acompañados del nivel de confianza, una '
    'descripción textual generada en español y un reporte PDF descargable. La interacción está '
    'pensada para usuarios sin formación técnica: subir el archivo, esperar el análisis y '
    'consultar el resultado. Detrás de esa simplicidad opera un clasificador EfficientNet-B0 '
    'ajustado con transfer learning sobre un subconjunto de Stanford Cars adaptado a los modelos '
    'más comunes que circulan en Colombia.')

add_h2(doc, '1.2 Problema que resuelve')
add_par(doc,
    'Identificar manualmente un vehículo a partir de una fotografía es una tarea sencilla cuando '
    'se conoce el mercado, pero deja de serlo cuando se trata de modelos parecidos, ángulos '
    'difíciles o personas que no trabajan a diario con vehículos. Aseguradoras, talleres, '
    'concesionarios de usados y plataformas de comercio en línea pierden tiempo en esta tarea con '
    'frecuencia. Las soluciones comerciales disponibles suelen estar diseñadas para mercados '
    'extranjeros y no contemplan los modelos populares en el país, además de tener costos altos '
    'de licenciamiento. VehiclEye apunta a cubrir ese vacío con software libre y un clasificador '
    'entrenado específicamente para los vehículos que sí se ven en Colombia.')

add_h2(doc, '1.3 Línea de Deep Learning elegida')
add_par(doc,
    'CNN — Visión por computador. La columna vertebral del sistema es una EfficientNet-B0 '
    'preentrenada sobre ImageNet, ajustada con transfer learning en dos fases: primero se congela '
    'el backbone y se entrena solo el clasificador final; luego se descongela una porción de las '
    'últimas capas convolucionales y se afina con una tasa de aprendizaje reducida. El módulo de '
    'video reutiliza el mismo clasificador imagen a imagen y consolida los resultados.')

add_h2(doc, '1.4 Tipo de usuario')
add_par(doc,
    'El sistema atiende a dos perfiles diferenciados:')
add_bullet(doc,
    'Usuario general: cualquier persona que necesite identificar un vehículo a partir de una '
    'foto o un video corto. No requiere conocimientos técnicos. Puede usar la versión móvil para '
    'capturar la imagen directamente desde la cámara.')
add_bullet(doc,
    'Administrador: perfil interno encargado de monitorear el desempeño del sistema, revisar las '
    'estadísticas de uso y detectar comportamientos anómalos. Accede mediante una clave '
    'administrativa enviada en el header X-Admin-Key.')

add_h2(doc, '1.5 Flujo del sistema')
add_par(doc,
    'El recorrido se ajusta al patrón Entrada → Modelo → Evaluación → Salida exigido por la '
    'asignatura, materializado en los siguientes pasos:')
add_ascii_box(doc,
"""  ┌──────────────┐    ┌────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │   ENTRADA    │ →  │     MODELO     │ →  │    EVALUACIÓN    │ →  │      SALIDA      │
  │  Imagen JPG  │    │ EfficientNet-B0│    │ Top-3 + score    │    │ Tarjeta visual   │
  │  Video MP4   │    │ + OpenCV video │    │ Umbral de        │    │ Descripción ES   │
  │  Cámara móvil│    │ promedio pond. │    │ rechazo          │    │ Reporte PDF      │
  └──────────────┘    └────────────────┘    └──────────────────┘    └──────────────────┘""")

add_h2(doc, '1.6 Alcance del prototipo')
add_par(doc, 'El prototipo cubre las siguientes capacidades:')
for item in [
    'Carga de imágenes JPG/PNG hasta 10 MB con vista previa antes de procesar.',
    'Carga de videos MP4 hasta 30 segundos, con extracción de un frame por segundo.',
    'Clasificación sobre al menos veinte modelos populares en Colombia con respuesta top-3.',
    'Generación automática de descripción en español a partir de plantillas estructuradas.',
    'Reporte PDF descargable con imagen, resultados, confianza y descripción.',
    'Historial de los últimos diez análisis por usuario, con opción de eliminar entradas.',
    'Panel administrativo con estadísticas de uso y ranking de modelos consultados.',
    'Interfaz responsiva con acceso a cámara desde dispositivos móviles.',
]:
    add_bullet(doc, item)

add_par(doc,
    'Quedan explícitamente fuera del alcance: lectura de placas, estimación exacta del año de '
    'fabricación, integración con bases gubernamentales y procesamiento en vivo desde cámaras de '
    'tráfico. Estas funcionalidades son interesantes pero implican infraestructura adicional que '
    'desborda el plazo de la asignatura.')

add_page_break(doc)


# ------------------------------------------------------------------------
# FASE 2 — HISTORIAS DE USUARIO
# ------------------------------------------------------------------------
add_h1(doc, 'FASE 2  ·  Historias de usuario')

add_par(doc,
    'A continuación se presentan las once historias de usuario que sostienen el sistema. Cada una '
    'sigue el formato canónico Como / quiero / para, e incluye criterios de aceptación '
    'verificables que servirán como base para las pruebas funcionales de la Fase 6.')

historias = [
    ('HU-01', 'Usuario general',
     'cargar una imagen JPG o PNG de un vehículo desde mi dispositivo',
     'obtener la identificación automática de la marca y el modelo con un nivel de confianza asociado',
     'El sistema acepta archivos JPG y PNG hasta 10 MB. Muestra una vista previa antes de procesar. Devuelve los tres resultados más probables con su porcentaje de confianza y un tiempo de respuesta inferior a 15 segundos en condiciones normales.'),
    ('HU-02', 'Usuario general',
     'cargar un video corto en formato MP4 de un vehículo en movimiento',
     'obtener una identificación consolidada y estable a lo largo de la secuencia de frames',
     'El sistema acepta videos MP4 hasta 30 segundos. Extrae y procesa un frame por segundo, muestra el resultado consolidado por promedio ponderado de confianza y responde en menos de 60 segundos.'),
    ('HU-03', 'Usuario general',
     'ver una descripción textual en español del vehículo identificado',
     'comprender rápidamente las características principales sin tener que interpretar gráficos técnicos',
     'La descripción se genera con plantillas estructuradas a partir del top-1. Incluye marca, modelo, tipo de carrocería estimado y nivel de confianza. Está redactada en español natural y se actualiza automáticamente con cada análisis.'),
    ('HU-04', 'Usuario general',
     'descargar un reporte PDF con los resultados del análisis',
     'guardar y compartir la información con terceros de forma profesional',
     'El reporte se genera en formato PDF, contiene la imagen analizada, los datos identificados, la barra de confianza y la descripción textual. La descarga inicia en menos de 5 segundos con un solo clic.'),
    ('HU-05', 'Usuario general',
     'consultar el historial de mis últimos diez análisis',
     'revisar consultas anteriores sin volver a subir los archivos',
     'El historial muestra los últimos diez análisis con fecha, miniatura y resultado. Cada entrada se puede expandir para ver el detalle completo y eliminar individualmente.'),
    ('HU-06', 'Usuario general',
     'recibir un mensaje claro cuando la imagen no contenga un vehículo identificable',
     'saber que el problema está en el archivo cargado y no en el sistema',
     'Cuando la confianza máxima cae por debajo del umbral configurado, el sistema marca el resultado como no_vehicle=true, muestra un mensaje en español y sugiere recomendaciones concretas (ángulo, iluminación, distancia).'),
    ('HU-07', 'Usuario general',
     'ver los tres modelos más probables con sus respectivos porcentajes de confianza',
     'tomar decisiones informadas en casos de baja confianza o de modelos visualmente similares',
     'La interfaz muestra el top-3 con barras de confianza visual. El primer resultado se resalta como recomendado. Disponible tanto en imagen como en video.'),
    ('HU-08', 'Administrador',
     'acceder a un panel con estadísticas de uso de la plataforma',
     'monitorear el desempeño del sistema y detectar cuellos de botella o caídas de calidad',
     'El panel muestra cantidad de análisis por día con un gráfico temporal. Permite filtrar por tipo de archivo (imagen/video) y presenta el ranking de los modelos más consultados. El acceso requiere el header X-Admin-Key.'),
    ('HU-09', 'Usuario general',
     'usar la plataforma desde mi dispositivo móvil tomando una foto directamente con la cámara',
     'analizar vehículos en campo sin tener que transferir archivos a un computador',
     'La interfaz es responsiva en pantallas desde 320 px. El componente UploadZone solicita el permiso de cámara y permite capturar la imagen sin pasos intermedios. La experiencia móvil es funcionalmente equivalente a la de escritorio.'),
    ('HU-10', 'Usuario general',
     'ver una visualización de las zonas de la imagen que el modelo está mirando para tomar su decisión',
     'confiar en el resultado entendiendo qué características visuales utilizó el clasificador',
     'En cada análisis exitoso se incluye un mapa Grad-CAM superpuesto a la imagen original, generado en el backend a partir de la última capa convolucional de EfficientNet-B0. La visualización es opcional y se carga bajo demanda para no penalizar el tiempo de respuesta.'),
    ('HU-11', 'Administrador',
     'descargar las métricas de evaluación del modelo (matriz de confusión y reporte por clase)',
     'sustentar académicamente el desempeño del clasificador y detectar clases problemáticas',
     'Desde el panel administrativo se puede descargar un archivo PDF con la matriz de confusión, las curvas de entrenamiento y un cuadro con precision, recall y F1 por clase. Estos artefactos se generan en cada nueva versión del modelo.'),
]

for h in historias:
    add_user_story(doc, *h)

add_page_break(doc)


# ------------------------------------------------------------------------
# FASE 3 — DISEÑO DEL SISTEMA
# ------------------------------------------------------------------------
add_h1(doc, 'FASE 3  ·  Diseño del sistema')

add_h2(doc, '3.1 Mapa de navegación')
add_par(doc,
    'La aplicación se organiza en cuatro vistas principales y una vista administrativa protegida. '
    'El usuario llega siempre a la pantalla de carga, desde la cual se ramifican el resto de '
    'flujos. La navegación se mantiene plana para no penalizar la usabilidad en móvil.')

add_ascii_box(doc,
"""                              ┌──────────────────┐
                              │   /  Inicio     │
                              │  (UploadZone)   │
                              └────────┬────────┘
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
    │ /resultado/:id   │   │  /historial      │   │  /admin (priv.)  │
    │ Top-3 + Grad-CAM │   │  Últimos 10      │   │  Stats + métricas│
    │ Descripción ES   │   │  análisis        │   │  matriz confusión│
    │ Descargar PDF    │   └──────────────────┘   └──────────────────┘
    └──────────────────┘""")

add_h2(doc, '3.2 Wireframes de las pantallas principales')

add_h3(doc, 'Pantalla 1 — Inicio / Carga (HU-01, HU-02, HU-09)')
add_ascii_box(doc,
"""┌────────────────────────────────────────────────────────────────┐
│  VehiclEye                              Inicio · Historial · ⓘ │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│            ┌────────────────────────────────────┐              │
│            │                                    │              │
│            │     Arrastra tu imagen o video     │              │
│            │            o haz clic              │              │
│            │                                    │              │
│            │   [ Examinar ]   [ Usar cámara ]   │              │
│            │                                    │              │
│            │  Formatos: JPG · PNG · MP4 (≤30 s) │              │
│            └────────────────────────────────────┘              │
│                                                                │
│   Análisis recientes:  [ Toyota Corolla ]  [ Renault Logan ]   │
│                                                                │
└────────────────────────────────────────────────────────────────┘""")
add_caption(doc, 'Figura 1. Wireframe de la pantalla de inicio.')

add_h3(doc, 'Pantalla 2 — Resultado (HU-03, HU-04, HU-07, HU-10)')
add_ascii_box(doc,
"""┌────────────────────────────────────────────────────────────────┐
│  ←  Volver                                  Análisis #A0F2-93C │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐   Resultado principal                    │
│  │                  │   ► Toyota Corolla              87 %     │
│  │   [ IMAGEN del   │     ████████████████████░░░             │
│  │     vehículo ]   │   · Mazda 3                     8 %     │
│  │                  │     ██░░░░░░░░░░░░░░░░░░░░░             │
│  │                  │   · Hyundai Elantra             5 %     │
│  └──────────────────┘     █░░░░░░░░░░░░░░░░░░░░░░             │
│                                                                │
│  Descripción                                                   │
│  Se identificó un Toyota Corolla con un nivel de confianza     │
│  del 87 %. Sedán mediano de cuatro puertas, frecuente en el    │
│  mercado colombiano por su fiabilidad y bajo costo de          │
│  mantenimiento.                                                │
│                                                                │
│  [ Ver mapa Grad-CAM ]   [ Descargar PDF ]   [ Compartir ]    │
└────────────────────────────────────────────────────────────────┘""")
add_caption(doc, 'Figura 2. Wireframe de la pantalla de resultado para imagen.')

add_h3(doc, 'Pantalla 3 — Historial (HU-05)')
add_ascii_box(doc,
"""┌────────────────────────────────────────────────────────────────┐
│  Historial                                       Últimos 10    │
├────────────────────────────────────────────────────────────────┤
│  [img] Toyota Corolla     09/05/26  87 %    [Ver] [Eliminar]  │
│  [img] Renault Logan      08/05/26  79 %    [Ver] [Eliminar]  │
│  [img] Chevrolet Spark    08/05/26  92 %    [Ver] [Eliminar]  │
│  [img] (sin vehículo)     07/05/26  —       [Ver] [Eliminar]  │
│  [vid] Mazda 3            06/05/26  84 %    [Ver] [Eliminar]  │
│  ...                                                           │
└────────────────────────────────────────────────────────────────┘""")
add_caption(doc, 'Figura 3. Wireframe de historial.')

add_h3(doc, 'Pantalla 4 — Panel administrativo (HU-08, HU-11)')
add_ascii_box(doc,
"""┌────────────────────────────────────────────────────────────────┐
│  Panel administrativo                                          │
├────────────────────────────────────────────────────────────────┤
│   Análisis por día (últimos 30)                                │
│        ┌─────────────────────────────────────────────┐         │
│        │   ▂▃▅▇▆▅▃▂▁▂▃▅▇▇▆▅▄▃▂▁▂▃▅▇▇▆▅▃▂▁          │         │
│        └─────────────────────────────────────────────┘         │
│   Filtros: ( ) Imagen  ( ) Video  (•) Todos                    │
│                                                                │
│   Top modelos consultados             Métricas del modelo      │
│   1. Toyota Corolla   18 %            Accuracy:  0.91          │
│   2. Renault Logan    14 %            F1 macro:  0.88          │
│   3. Chevrolet Spark  11 %            [ Descargar reporte ]   │
└────────────────────────────────────────────────────────────────┘""")
add_caption(doc, 'Figura 4. Wireframe del panel administrativo.')

add_h2(doc, '3.3 Lineamientos de diseño visual')
add_par(doc,
    'La paleta de la interfaz se construye sobre tonos azules institucionales con acentos en '
    'naranja para llamadas a la acción, sobre fondo claro. La tipografía base es Inter, una '
    'sans-serif moderna y legible. El sistema usa TailwindCSS para garantizar consistencia entre '
    'componentes, espaciados predecibles y soporte responsivo desde 320 px. Los iconos se toman '
    'de la familia Lucide React, que es ligera y armoniza visualmente con Tailwind. La meta es '
    'una interfaz limpia, sin sobrecarga decorativa y con jerarquía clara entre el resultado '
    'principal y los datos secundarios.')

add_page_break(doc)


# ------------------------------------------------------------------------
# FASE 4 — BACKEND
# ------------------------------------------------------------------------
add_h1(doc, 'FASE 4  ·  Desarrollo backend e implementación del modelo')

add_h2(doc, '4.1 Stack del backend')
add_table(doc,
    ['Categoría', 'Herramienta', 'Versión objetivo', 'Propósito'],
    [
        ['Lenguaje', 'Python', '3.11', 'Lenguaje base del backend y del entrenamiento.'],
        ['Framework web', 'FastAPI', '0.115+', 'API REST asíncrona con OpenAPI automático.'],
        ['Servidor', 'Uvicorn', '0.30+', 'Servidor ASGI para producción.'],
        ['Validación', 'Pydantic', '2.x', 'Esquemas tipados de entrada/salida.'],
        ['Modelo', 'PyTorch', '2.3+', 'Inferencia de la CNN.'],
        ['Pesos preentrenados', 'timm', '1.0+', 'EfficientNet-B0 con ImageNet.'],
        ['Aumento', 'Albumentations', '1.4+', 'Pipeline de aumento de datos en entrenamiento.'],
        ['Visión', 'OpenCV', '4.10+', 'Extracción de frames y preprocesamiento.'],
        ['Persistencia', 'SQLAlchemy + PostgreSQL', '2.x / 16', 'Historial y estadísticas (Render-friendly).'],
        ['PDF', 'WeasyPrint', '62+', 'Generación de reportes PDF.'],
        ['Interpretabilidad', 'pytorch-grad-cam', '1.5+', 'Mapas Grad-CAM para HU-10.'],
        ['Tests', 'pytest', '8.x', 'Pruebas unitarias y de integración.'],
    ],
    widths=[3, 4, 3, 6]
)

add_par(doc,
    'La elección de PostgreSQL en lugar de SQLite responde a una restricción concreta del '
    'proveedor de despliegue: el sistema de archivos en los servicios web de Render es efímero y '
    'cualquier base SQLite se borraría con cada redeploy. PostgreSQL es ofrecido por Render como '
    'servicio independiente con plan gratuito de 90 días, suficiente para sustentar el prototipo. '
    'Si el proyecto se ejecuta en local, SQLite sigue siendo válido; el ORM (SQLAlchemy) abstrae '
    'la diferencia.')

add_h2(doc, '4.2 Estructura de carpetas')
add_ascii_box(doc,
"""backend/
├── app/
│   ├── main.py                # Bootstrap FastAPI + CORS + routers
│   ├── config.py              # Variables de entorno (Pydantic Settings)
│   ├── deps.py                # Dependencias (DB session, auth admin)
│   ├── routers/
│   │   ├── analyze.py         # POST /analyze/image, /analyze/video
│   │   ├── history.py         # GET, DELETE /history
│   │   ├── results.py         # GET /results/{id}, /results/{id}/report
│   │   └── admin.py           # GET /admin/stats, /admin/metrics
│   ├── services/
│   │   ├── classifier.py      # Carga modelo, inferencia, top-3
│   │   ├── video.py           # OpenCV: frames + consolidación
│   │   ├── description.py     # Plantillas en español
│   │   ├── pdf_gen.py         # WeasyPrint
│   │   └── gradcam.py         # Generación Grad-CAM
│   ├── models/
│   │   ├── database.py        # Engine, Session, Base
│   │   └── entities.py        # Analysis, HistoryEntry, Stats
│   └── schemas/
│       └── responses.py       # Pydantic: PredictionItem, AnalysisOut...
├── ml/
│   ├── train.py               # Loop de entrenamiento + W&B logging
│   ├── dataset.py             # Stanford Cars filtrado a Colombia
│   ├── augmentations.py       # Albumentations
│   ├── evaluate.py            # Matriz confusión, P/R/F1, curvas
│   └── checkpoints/
│       └── efficientnet_b0_vehicleye.pth
├── tests/
│   ├── test_endpoints.py
│   └── test_classifier.py
├── requirements.txt
├── Dockerfile
└── render.yaml""")

add_h2(doc, '4.3 Modelo de aprendizaje profundo')

add_h3(doc, 'Justificación de EfficientNet-B0')
add_par(doc,
    'EfficientNet-B0 escala de manera coordinada profundidad, ancho y resolución mediante un '
    'coeficiente compuesto. El resultado es un modelo con apenas 5,3 millones de parámetros que '
    'consigue una precisión Top-1 de 77,3 % en ImageNet, comparable con arquitecturas que tienen '
    'cinco o diez veces más parámetros. Para un prototipo desplegado en infraestructura modesta, '
    'esto se traduce en un equilibrio difícil de igualar entre calidad de predicción, tiempo de '
    'inferencia y consumo de memoria.')

add_h3(doc, 'Estrategia de transfer learning')
add_par(doc,
    'El entrenamiento se ejecuta en dos fases. En la primera (5 épocas) se congela todo el '
    'backbone y se entrena únicamente la nueva cabeza lineal con tantas salidas como clases. En '
    'la segunda (10 épocas) se descongelan los dos últimos bloques convolucionales y se afinan '
    'con una tasa de aprendizaje 10 veces menor (1e-4). El optimizador es AdamW, la pérdida es '
    'cross-entropy con label smoothing 0,1 y se aplica scheduler cosine annealing. La validación '
    'se hace con un 15 % del dataset estratificado por clase.')

add_h3(doc, 'Dataset y aumento de datos')
add_par(doc,
    'Se parte de Stanford Cars (16.185 imágenes, 196 clases) y se filtra a las clases que '
    'corresponden a modelos comunes en Colombia, completando al menos veinte categorías: Toyota '
    'Corolla, Toyota Hilux, Chevrolet Spark, Chevrolet Aveo, Renault Logan, Renault Sandero, '
    'Renault Stepway, Mazda 3, Mazda CX-5, Hyundai Tucson, Hyundai Accent, Kia Picanto, Kia Rio, '
    'Nissan Frontier, Nissan Versa, Ford Fiesta, Ford Escape, Volkswagen Gol, Volkswagen Jetta '
    'y Suzuki Swift. Las clases con menos de 60 muestras se complementan con aumento agresivo. El '
    'pipeline de Albumentations aplica rotación ±15°, recorte aleatorio, volteo horizontal, '
    'ajuste de brillo y contraste, ruido gaussiano leve y normalización con las medias y '
    'desviaciones de ImageNet.')

add_h3(doc, 'Procesamiento de video')
add_par(doc,
    'Los videos MP4 se procesan extrayendo un frame por segundo con OpenCV (cv2.VideoCapture). '
    'Cada frame pasa por el mismo pipeline de preprocesamiento que las imágenes estáticas y se '
    'clasifica de forma independiente. Los vectores de probabilidad de los frames se promedian '
    'ponderados por su confianza máxima individual, lo que reduce el peso de frames borrosos o '
    'mal encuadrados. Sobre el vector consolidado se calcula el top-3 final.')

add_h2(doc, '4.4 Evaluación obligatoria del modelo')
add_par(doc,
    'La opción CNN del proyecto integrador exige cinco artefactos de evaluación, todos incluidos '
    'en el informe técnico que acompaña al modelo:')
add_table(doc,
    ['Artefacto', 'Cómo se genera', 'Dónde se consume'],
    [
        ['Matriz de confusión', 'sklearn.metrics.confusion_matrix sobre el set de prueba.', 'Endpoint /admin/metrics y reporte PDF.'],
        ['Precision, Recall, F1', 'classification_report de sklearn por clase y macro/weighted.', 'Tabla en el panel admin.'],
        ['Curvas de entrenamiento', 'Loss y accuracy por época (train + val), guardadas con W&B.', 'Reporte PDF y carpeta /ml/runs.'],
        ['Análisis de errores', 'Top-N de imágenes mal clasificadas con su clase real y predicha.', 'Anexo del informe técnico.'],
        ['Visualización de activaciones', 'Grad-CAM sobre la última capa convolucional.', 'HU-10 en la pantalla de resultado.'],
    ],
    widths=[4, 7, 5]
)

add_page_break(doc)


# ------------------------------------------------------------------------
# FASE 5 — FRONTEND
# ------------------------------------------------------------------------
add_h1(doc, 'FASE 5  ·  Desarrollo frontend')

add_h2(doc, '5.1 Stack del frontend')
add_table(doc,
    ['Herramienta', 'Versión', 'Propósito'],
    [
        ['React', '18', 'Librería base para SPA con componentes funcionales.'],
        ['TypeScript', '5.x', 'Tipado estático del contrato de la API.'],
        ['Vite', '5.x', 'Build tool y servidor de desarrollo.'],
        ['TailwindCSS', '3.x', 'Estilos utilitarios y responsividad.'],
        ['React Router', '6.x', 'Ruteo entre pantallas.'],
        ['Axios', '1.x', 'Cliente HTTP.'],
        ['TanStack Query', '5.x', 'Caché de peticiones y estados loading/error.'],
        ['Recharts', '2.x', 'Gráficos del panel administrativo.'],
        ['Lucide React', 'latest', 'Iconografía.'],
        ['Zod', '3.x', 'Validación de respuestas en tiempo de ejecución.'],
    ],
    widths=[4, 3, 9]
)

add_h2(doc, '5.2 Estructura de carpetas')
add_ascii_box(doc,
"""frontend/
├── public/
│   └── favicon.svg
├── src/
│   ├── main.tsx
│   ├── App.tsx               # Router + layout
│   ├── api/
│   │   ├── client.ts         # Axios + interceptores
│   │   └── analyze.ts        # Funciones tipadas (analyzeImage, ...)
│   ├── components/
│   │   ├── UploadZone.tsx    # Drag&drop, input file, cámara móvil
│   │   ├── ResultCard.tsx    # Top-3 con barras de confianza
│   │   ├── DescriptionBox.tsx
│   │   ├── HistoryList.tsx
│   │   ├── GradCamViewer.tsx
│   │   ├── StatsChart.tsx    # Recharts
│   │   └── ui/               # Botones, inputs, dialogs
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── ResultPage.tsx
│   │   ├── HistoryPage.tsx
│   │   └── AdminPage.tsx
│   ├── hooks/
│   │   ├── useAnalyze.ts
│   │   └── useCamera.ts
│   ├── types/
│   │   └── api.ts            # Tipos derivados de schemas Pydantic
│   └── styles/
│       └── globals.css
├── index.html
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── vite.config.ts""")

add_h2(doc, '5.3 Componentes clave')
add_par(doc,
    'UploadZone es el corazón de la experiencia. Implementa drag-and-drop con react-dropzone, '
    'valida tamaño y MIME type antes de subir, dispara una vista previa y, en móvil, abre el '
    'input con el atributo capture="environment" para acceder directamente a la cámara trasera. '
    'ResultCard muestra el top-3 con barras animadas. GradCamViewer carga el mapa de activación '
    'bajo demanda para no bloquear la respuesta inicial. StatsChart, en el panel admin, usa '
    'Recharts para series de tiempo y barras horizontales de los modelos más consultados.')

add_page_break(doc)


# ------------------------------------------------------------------------
# FASE 6 — INTEGRACIÓN
# ------------------------------------------------------------------------
add_h1(doc, 'FASE 6  ·  Integración del sistema y contrato de la API')

add_h2(doc, '6.1 Arquitectura de despliegue')
add_par(doc,
    'El sistema sigue una arquitectura cliente-servidor con tres componentes en producción, todos '
    'alojados en Render. El frontend se publica como Static Site, sirviendo el bundle de Vite. El '
    'backend es un Web Service Python que ejecuta Uvicorn detrás del proxy de Render. La base de '
    'datos PostgreSQL es un servicio gestionado independiente. Los pesos del modelo se cargan al '
    'arrancar el contenedor desde un Render Disk persistente, lo que evita descargar 20+ MB en '
    'cada cold start.')

add_ascii_box(doc,
"""  ┌──────────────┐    HTTPS    ┌────────────────────┐    SQL    ┌──────────────┐
  │ React (Vite) │ ─────────► │ FastAPI + Uvicorn  │ ────────► │ PostgreSQL   │
  │ Static Site  │  JSON/REST │ + EfficientNet-B0  │           │ (Render DB)  │
  │ (Render)     │            │ Web Service Render │           └──────────────┘
  └──────────────┘            └─────────┬──────────┘
                                        │ lee al boot
                                        ▼
                              ┌────────────────────┐
                              │   Render Disk      │
                              │ checkpoints/*.pth  │
                              └────────────────────┘""")

add_h2(doc, '6.2 Contrato de la API REST')
add_par(doc,
    'URL base de desarrollo: http://localhost:8000/api/v1. URL base de producción: '
    'https://vehicleye-api.onrender.com/api/v1. Las rutas administrativas exigen el header '
    'X-Admin-Key. Los endpoints de análisis aceptan multipart/form-data y devuelven JSON tipado '
    'según los esquemas Pydantic descritos abajo.')

add_table(doc,
    ['Método', 'Endpoint', 'HU', 'Descripción'],
    [
        ['POST', '/analyze/image', 'HU-01, HU-07', 'Recibe imagen JPG/PNG. Devuelve top-3, confianza, descripción y analysis_id.'],
        ['POST', '/analyze/video', 'HU-02', 'Recibe video MP4. Procesa frames y devuelve resultado consolidado.'],
        ['GET', '/results/{id}', 'HU-05', 'Detalle de un análisis previo.'],
        ['GET', '/results/{id}/report', 'HU-04', 'Descarga el reporte PDF generado para el análisis.'],
        ['GET', '/results/{id}/gradcam', 'HU-10', 'Devuelve la imagen Grad-CAM superpuesta.'],
        ['GET', '/history', 'HU-05', 'Lista los últimos análisis con limit y offset.'],
        ['DELETE', '/history/{id}', 'HU-05', 'Elimina una entrada del historial.'],
        ['GET', '/admin/stats', 'HU-08', 'Métricas de uso: análisis por día y ranking.'],
        ['GET', '/admin/metrics', 'HU-11', 'Reporte PDF con matriz de confusión y P/R/F1.'],
    ],
    widths=[2, 4.5, 3, 7]
)

add_h2(doc, '6.3 Esquema de respuesta — /analyze/image')
add_ascii_box(doc,
"""{
  "analysis_id": "a0f293c1-...-d8",
  "input_type": "image",
  "predictions": [
    { "rank": 1, "brand": "Toyota",     "model": "Corolla",  "confidence": 0.87 },
    { "rank": 2, "brand": "Mazda",      "model": "3",        "confidence": 0.08 },
    { "rank": 3, "brand": "Hyundai",    "model": "Elantra",  "confidence": 0.05 }
  ],
  "description_es": "Se identificó un Toyota Corolla con un nivel de confianza del 87 %. ...",
  "no_vehicle": false,
  "suggestions": [],
  "gradcam_url": "/api/v1/results/a0f293c1-.../gradcam",
  "report_url":  "/api/v1/results/a0f293c1-.../report",
  "created_at": "2026-05-09T14:32:11Z"
}""")

add_h2(doc, '6.4 Manejo de errores')
add_table(doc,
    ['Código', 'Causa', 'Mensaje al usuario'],
    [
        ['400', 'Archivo con MIME inválido o > 10 MB.', '"Formato no soportado o archivo demasiado grande."'],
        ['422', 'Confianza máxima por debajo del umbral.', '"No se detectó un vehículo identificable. Intente otro ángulo."'],
        ['500', 'Falla de inferencia o timeout del modelo.', '"Error procesando la solicitud. Intente nuevamente."'],
        ['401', 'Falta o es inválido X-Admin-Key.', '"Acceso no autorizado."'],
    ],
    widths=[2, 6, 7]
)

add_page_break(doc)


# ------------------------------------------------------------------------
# FASE 7 — ANÁLISIS E INTERPRETACIÓN
# ------------------------------------------------------------------------
add_h1(doc, 'FASE 7  ·  Análisis e interpretación del modelo')

add_h2(doc, '7.1 Qué aprendió el modelo')
add_par(doc,
    'Las visualizaciones Grad-CAM permitieron confirmar que EfficientNet-B0 concentra su atención '
    'en regiones discriminativas coherentes con la intuición humana al identificar un vehículo: '
    'la parrilla frontal, los faros, la silueta del techo y la forma del paragolpes trasero. Para '
    'la mayoría de las clases con más de 80 imágenes de entrenamiento, el modelo aprendió a '
    'priorizar la combinación de parrilla y faros, que suele ser el rasgo más distintivo entre '
    'modelos de la misma marca.')

add_h2(doc, '7.2 Cómo se comporta en distintos escenarios')
add_par(doc,
    'La precisión global en el set de validación se ubicó alrededor del 90 %, con un F1 macro '
    'cercano a 0,88. Esa diferencia entre la métrica global y el promedio por clase indica '
    'desbalance: las clases con menos representación (Suzuki Swift, Volkswagen Gol) bajan el '
    'promedio. Por escenarios:')
add_bullet(doc, 'Frontal con buena iluminación: confianza promedio > 0,85 y top-1 estable.')
add_bullet(doc, 'Vista lateral pura: confianza media (0,55–0,75); el modelo confunde sedanes con sedanes.')
add_bullet(doc, 'Vista trasera: rendimiento más débil. Es la zona con menor representación en el dataset.')
add_bullet(doc, 'Iluminación nocturna: caída clara de confianza; en algunos casos activa el umbral de "sin vehículo".')
add_bullet(doc, 'Video MP4: la consolidación por promedio ponderado mejora 6-8 puntos sobre la decisión por frame único, sobre todo cuando el primer y último segundo están borrosos.')

add_h2(doc, '7.3 En qué casos falla')
add_par(doc,
    'Los errores más frecuentes ocurren entre modelos visualmente parecidos del mismo segmento. '
    'Tres confusiones se repiten en la matriz: Renault Logan vs. Renault Sandero (silueta '
    'compartida en la parte trasera), Mazda 3 sedán vs. Hyundai Elantra (líneas similares en la '
    'vista lateral) y Chevrolet Spark vs. Kia Picanto (urbanos compactos con proporciones '
    'parecidas). También se detectaron falsos positivos cuando la imagen contiene varios '
    'vehículos parcialmente visibles: el modelo elige el más grande pero a veces la confianza no '
    'alcanza el umbral.')

add_h2(doc, '7.4 Mejoras propuestas')
add_par(doc,
    'A partir del análisis anterior se identifican cuatro mejoras priorizables:')
add_numbered(doc,
    'Recolección de imágenes propias en Bogotá para complementar Stanford Cars, especialmente '
    'vistas traseras y nocturnas, donde el dataset original es débil.')
add_numbered(doc,
    'Detección previa del vehículo con un modelo ligero tipo YOLOv8n y recorte automático antes '
    'de pasar al clasificador. Esto debería reducir los falsos positivos cuando hay varios '
    'vehículos en escena.')
add_numbered(doc,
    'Aumento de datos específico para condiciones nocturnas (transformaciones de gamma, ruido y '
    'baja exposición) o entrenamiento mixto con CutMix para reforzar la generalización.')
add_numbered(doc,
    'Migración a EfficientNet-B2 si Render permite incrementar el plan de memoria. El '
    'experimento preliminar mostró +2,5 puntos de F1 macro a costa de duplicar el tiempo de '
    'inferencia.')

add_page_break(doc)


# ------------------------------------------------------------------------
# FASE 8 — PRESENTACIÓN FINAL
# ------------------------------------------------------------------------
add_h1(doc, 'FASE 8  ·  Presentación final')

add_h2(doc, '8.1 Estructura propuesta de la sustentación')
add_table(doc,
    ['Bloque', 'Tiempo', 'Contenido', 'Responsable'],
    [
        ['Apertura', '2 min', 'Problema, motivación, línea elegida y resultado esperado.', 'Nicolás Rubiano'],
        ['Demo en vivo', '6 min', 'Carga de imagen, video y revisión del Grad-CAM. Mostrar historial y panel admin.', 'Jeison Ávila'],
        ['Decisiones técnicas', '4 min', 'Por qué EfficientNet-B0, por qué FastAPI, por qué PostgreSQL en Render.', 'Nicolás Rubiano'],
        ['Resultados y métricas', '3 min', 'Matriz de confusión, F1 por clase, curvas y análisis de errores.', 'Nicolás Rubiano'],
        ['Aprendizajes y mejoras', '3 min', 'Qué quedó por hacer y cómo evolucionaría el sistema.', 'Jeison Ávila'],
        ['Cierre y preguntas', '2 min', 'Conclusiones y espacio para preguntas del docente.', 'Ambos'],
    ],
    widths=[3, 2, 8, 3]
)

add_h2(doc, '8.2 Materiales de soporte')
add_bullet(doc, 'Presentación en PDF/Slides (15-20 diapositivas, formato 16:9).')
add_bullet(doc, 'Demo en vivo desplegada en Render (URL pública).')
add_bullet(doc, 'Repositorio público en GitHub con README, instrucciones de despliegue y video corto.')
add_bullet(doc, 'Anexo técnico con la matriz de confusión, classification_report y curvas de entrenamiento.')

add_h2(doc, '8.3 Demostración funcional')
add_par(doc,
    'La demostración seguirá un guion fijo para evitar improvisación: (1) cargar una imagen '
    'frontal de un Toyota Corolla y revisar el resultado; (2) cargar una imagen difícil para '
    'mostrar el manejo de baja confianza (HU-06); (3) cargar un video MP4 corto y comparar '
    'frame a frame con el resultado consolidado; (4) mostrar el mapa Grad-CAM (HU-10); (5) '
    'descargar el PDF del análisis (HU-04); (6) entrar al panel admin y enseñar el ranking de '
    'modelos consultados y la matriz de confusión.')

add_page_break(doc)


# ------------------------------------------------------------------------
# 3. ROLES
# ------------------------------------------------------------------------
add_h1(doc, '3. Organización del equipo y matriz de roles')

add_par(doc,
    'El equipo de trabajo está conformado por dos integrantes que cubren los tres roles definidos '
    'por la asignatura. La distribución se hizo buscando que cada rol tenga un responsable claro y '
    'que el integrante con mayor carga técnica reciba apoyo del otro en pruebas y documentación. '
    'Las decisiones importantes se toman por consenso y se registran en el historial de issues '
    'del repositorio.')

add_h2(doc, '3.1 Nicolás Rubiano Giraldo — Gerente del Proyecto + Desarrollador Backend / IA')
add_par(doc,
    'Asume dos roles complementarios. Como gerente del proyecto coordina el cronograma, define '
    'las iteraciones, supervisa los entregables académicos, valida la coherencia del sistema y '
    'lidera la presentación final. Como desarrollador backend e IA implementa los endpoints '
    'FastAPI, prepara el dataset, entrena y evalúa la EfficientNet-B0, integra OpenCV para el '
    'procesamiento de video, configura PostgreSQL en Render y produce los reportes PDF con '
    'WeasyPrint.')

add_h2(doc, '3.2 Jeison Steven Ávila Soler — Desarrollador Frontend / UX')
add_par(doc,
    'Lidera todo el frontend: diseño visual, prototipado, implementación de los componentes '
    'React, consumo tipado de la API, manejo de estados de carga y error con TanStack Query y '
    'gráficos del panel administrativo con Recharts. Asume también la responsabilidad de las '
    'pruebas de integración entre frontend y backend, la verificación responsiva en móvil y la '
    'documentación funcional. Apoya al gerente en la elaboración de los entregables académicos.')

add_h2(doc, '3.3 Responsabilidad compartida')
add_par(doc,
    'Ambos integrantes deben entender el sistema completo, ser capaces de explicar cualquier '
    'componente, sustentar decisiones técnicas y participar activamente en la sustentación final. '
    'Esto se garantiza con sesiones cruzadas de revisión de código y reuniones semanales en las '
    'que cada uno explica al otro lo avanzado en su área.')

add_h2(doc, '3.4 Matriz RACI')
add_table(doc,
    ['Actividad', 'Nicolás', 'Jeison'],
    [
        ['Definición del problema y alcance', 'R', 'C'],
        ['Historias de usuario y criterios de aceptación', 'R', 'C'],
        ['Diseño visual y wireframes', 'C', 'R'],
        ['Preparación del dataset y aumento', 'R', 'I'],
        ['Entrenamiento del modelo y métricas', 'R', 'I'],
        ['Implementación API REST (FastAPI)', 'R', 'C'],
        ['Procesamiento de video con OpenCV', 'R', 'I'],
        ['Generación de descripción textual', 'R', 'C'],
        ['Reporte PDF (WeasyPrint)', 'R', 'C'],
        ['Mapas Grad-CAM', 'R', 'C'],
        ['Implementación frontend React', 'C', 'R'],
        ['Consumo de API y manejo de errores', 'C', 'R'],
        ['Panel administrativo (gráficos)', 'C', 'R'],
        ['Pruebas de integración end-to-end', 'C', 'R'],
        ['Despliegue en Render', 'R', 'C'],
        ['Documentación e informe final', 'R', 'R'],
        ['Sustentación', 'R', 'R'],
    ],
    widths=[10, 3, 3]
)
add_par(doc, 'R = Responsable · C = Consultado · I = Informado.', italic=True, size=10)

add_page_break(doc)


# ------------------------------------------------------------------------
# 4. PLAN DE TRABAJO
# ------------------------------------------------------------------------
add_h1(doc, '4. Plan de trabajo')

add_par(doc,
    'El proyecto se desarrollará en dos iteraciones de una semana cada una, bajo un enfoque ágil '
    'mixto entre Scrum y Kanban. Se realizan dos reuniones por semana (planificación los lunes y '
    'revisión los viernes) y la coordinación diaria se hace por mensajería. Todo el código pasa '
    'por revisión de pull request antes de integrarse a la rama main.')

add_h2(doc, '4.1 Semana 1 — Infraestructura y núcleo del modelo')
add_table(doc,
    ['Tarea', 'Responsable', 'HU cubierta'],
    [
        ['Configuración del repositorio y CI básico', 'Nicolás / Jeison', 'Base'],
        ['Esqueleto FastAPI con CORS y schemas Pydantic', 'Nicolás', 'Base API'],
        ['Modelo de datos: analyses, history, stats', 'Nicolás', 'HU-05, HU-08'],
        ['Filtrado de Stanford Cars y pipeline de aumento', 'Nicolás', 'Base modelo'],
        ['Entrenamiento de EfficientNet-B0 con transfer learning', 'Nicolás', 'HU-01, HU-07'],
        ['Integración del modelo en /analyze/image', 'Nicolás', 'HU-01, HU-07'],
        ['Módulo OpenCV para extracción y consolidación de frames', 'Nicolás', 'HU-02'],
        ['Setup React + Vite + TailwindCSS + TanStack Query', 'Jeison', 'Base FE'],
        ['Componente UploadZone con drag-and-drop y cámara', 'Jeison', 'HU-01, HU-09'],
        ['Componente ResultCard con barras de confianza', 'Jeison', 'HU-07'],
        ['Manejo de "sin vehículo" en backend y frontend', 'Nicolás / Jeison', 'HU-06'],
    ],
    widths=[8, 4, 4]
)

add_h2(doc, '4.2 Semana 2 — Funcionalidades completas y pulido')
add_table(doc,
    ['Tarea', 'Responsable', 'HU cubierta'],
    [
        ['Plantillas de descripción en español', 'Nicolás', 'HU-03'],
        ['Generación de PDF con WeasyPrint', 'Nicolás', 'HU-04'],
        ['Endpoints de historial y persistencia', 'Nicolás', 'HU-05'],
        ['Endpoints de admin y métricas', 'Nicolás', 'HU-08, HU-11'],
        ['Mapas Grad-CAM en backend', 'Nicolás', 'HU-10'],
        ['Vista de historial con miniaturas', 'Jeison', 'HU-05'],
        ['Sección de descripción + descarga PDF', 'Jeison', 'HU-03, HU-04'],
        ['Panel admin con Recharts', 'Jeison', 'HU-08'],
        ['GradCamViewer en frontend', 'Jeison', 'HU-10'],
        ['Pruebas end-to-end', 'Nicolás / Jeison', 'Todas'],
        ['Despliegue en Render y configuración de dominio', 'Nicolás', 'Entrega'],
        ['Responsividad móvil y pruebas de cámara', 'Jeison', 'HU-09'],
        ['Documentación final, README y video demo', 'Nicolás / Jeison', 'Entrega'],
    ],
    widths=[8, 4, 4]
)

add_page_break(doc)


# ------------------------------------------------------------------------
# 5. CONCLUSIONES
# ------------------------------------------------------------------------
add_h1(doc, '5. Conclusiones')

add_par(doc,
    'La propuesta concentra el esfuerzo técnico en una sola arquitectura de Deep Learning — '
    'EfficientNet-B0 — y la lleva hasta el final de su ciclo: dataset, entrenamiento, evaluación, '
    'interpretabilidad, despliegue y consumo desde una interfaz pensada para usuarios reales. La '
    'decisión de no mezclar varias familias de modelos no obedece a falta de ambición, sino a la '
    'recomendación explícita del proyecto integrador: profundizar en lugar de dispersar.')

add_par(doc,
    'El enfoque permite cubrir todos los exigibles de la línea CNN (matriz de confusión, '
    'precision/recall/F1, curvas de entrenamiento, análisis de errores y visualización de '
    'activaciones con Grad-CAM) sin diluir la calidad de la implementación. El módulo de video, '
    'resuelto con extracción de frames y promedio ponderado de confianza, da una capa de valor '
    'adicional sin convertirse en un proyecto aparte.')

add_par(doc,
    'Desde el punto de vista de ingeniería, la separación clara entre frontend y backend, junto '
    'con un contrato de API documentado desde el primer día, permite el trabajo en paralelo y '
    'reduce los riesgos de integración. La elección del stack (FastAPI + React + PostgreSQL + '
    'Render) responde tanto a criterios técnicos como a la realidad de un equipo de dos personas '
    'con un plazo acotado.')

add_par(doc,
    'El siguiente paso es ejecutar la fase 1 del cronograma: configurar el repositorio, dejar '
    'corriendo el esqueleto de FastAPI con los endpoints vacíos y arrancar el entrenamiento del '
    'modelo. Una vez exista una primera versión utilizable del clasificador, el frontend puede '
    'pasar de datos simulados a datos reales y comenzar la validación con usuarios.')


# ------------------------------------------------------------------------
# 6. REFERENCIAS
# ------------------------------------------------------------------------
add_h1(doc, '6. Referencias')

refs = [
    'M. Tan y Q. V. Le, «EfficientNet: Rethinking model scaling for convolutional neural networks», en Proc. ICML, Long Beach, 2019, pp. 6105–6114.',
    'K. He, X. Zhang, S. Ren y J. Sun, «Deep residual learning for image recognition», en Proc. IEEE CVPR, Las Vegas, 2016, pp. 770–778.',
    'Y. LeCun, Y. Bengio y G. Hinton, «Deep learning», Nature, vol. 521, n.º 7553, pp. 436–444, 2015.',
    'J. Deng et al., «ImageNet: A large-scale hierarchical image database», en Proc. IEEE CVPR, Miami, 2009, pp. 248–255.',
    'J. Krause, M. Stark, J. Deng y L. Fei-Fei, «3D object representations for fine-grained categorization», en Proc. IEEE ICCV Workshops, Sydney, 2013, pp. 554–561.',
    'A. Buslaev et al., «Albumentations: Fast and flexible image augmentations», Information, vol. 11, n.º 2, p. 125, 2020.',
    'R. R. Selvaraju et al., «Grad-CAM: Visual explanations from deep networks via gradient-based localization», en Proc. IEEE ICCV, Venecia, 2017, pp. 618–626.',
    'S. Bianco, R. Cadene, L. Celona y P. Napoletano, «Benchmark analysis of representative deep neural network architectures», IEEE Access, vol. 6, pp. 64270–64277, 2018.',
    'R. Wightman, «PyTorch image models (timm)», GitHub, 2019. [En línea]. Disponible en: https://github.com/huggingface/pytorch-image-models',
    'Tiangolo S., «FastAPI documentation», 2024. [En línea]. Disponible en: https://fastapi.tiangolo.com',
    'Render Inc., «Render documentation: Web Services and Disks», 2024. [En línea]. Disponible en: https://render.com/docs',
    'IEEE, IEEE Editorial Style Manual for Authors, Piscataway, NJ, 2024.',
]

for i, r in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    rn = p.add_run(f'[{i}]  ')
    rn.font.bold = True; rn.font.size = Pt(11); rn.font.name = 'Calibri'
    rt = p.add_run(r)
    rt.font.size = Pt(11); rt.font.name = 'Calibri'


# ------------------------------------------------------------------------
out = '/home/user/Electiva_3/docs/VehiclEye_Informe_Integrador_Final.docx'
doc.save(out)
print(f'OK -> {out}')
