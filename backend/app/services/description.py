"""
Genera descripciones textuales en español a partir de los resultados del clasificador.
Se usa un sistema de plantillas estructuradas para garantizar consistencia y legibilidad.
"""
from __future__ import annotations

from app.services.classifier import Prediction


_BODY_TYPE: dict[tuple[str, str], str] = {
    ("Toyota", "Corolla"):      "sedán mediano de cuatro puertas",
    ("Toyota", "Hilux"):        "camioneta pick-up doble cabina",
    ("Chevrolet", "Spark"):     "hatchback urbano de cinco puertas",
    ("Chevrolet", "Aveo"):      "sedán compacto de cuatro puertas",
    ("Renault", "Logan"):       "sedán compacto de cuatro puertas",
    ("Renault", "Sandero"):     "hatchback compacto de cinco puertas",
    ("Renault", "Stepway"):     "crossover compacto de cinco puertas",
    ("Mazda", "3"):             "sedán o hatchback compacto",
    ("Mazda", "CX-5"):          "SUV mediano de cinco puertas",
    ("Hyundai", "Tucson"):      "SUV mediano de cinco puertas",
    ("Hyundai", "Accent"):      "sedán compacto de cuatro puertas",
    ("Kia", "Picanto"):         "hatchback urbano de cinco puertas",
    ("Kia", "Rio"):             "sedán o hatchback compacto",
    ("Nissan", "Frontier"):     "camioneta pick-up doble cabina",
    ("Nissan", "Versa"):        "sedán compacto de cuatro puertas",
    ("Ford", "Fiesta"):         "hatchback compacto de cinco puertas",
    ("Ford", "Escape"):         "SUV compacto de cinco puertas",
    ("Volkswagen", "Gol"):      "hatchback compacto de cinco puertas",
    ("Volkswagen", "Jetta"):    "sedán mediano de cuatro puertas",
    ("Suzuki", "Swift"):        "hatchback compacto de cinco puertas",
}

_CONFIDENCE_LABEL: list[tuple[float, str]] = [
    (0.85, "muy alta"),
    (0.65, "alta"),
    (0.45, "moderada"),
    (0.25, "baja"),
    (0.0,  "muy baja"),
]

_NO_VEHICLE_MSG = (
    "No fue posible identificar un vehículo en el archivo cargado con suficiente certeza. "
    "Esto puede deberse a que la imagen no contiene un automóvil, el ángulo de captura no "
    "permite reconocer las características del vehículo, o las condiciones de iluminación "
    "no son las adecuadas."
)

_SUGGESTIONS = [
    "Capture el vehículo de frente o en ángulo de tres cuartos.",
    "Asegúrese de que el vehículo ocupe al menos el 40 % del encuadre.",
    "Evite capturas nocturnas o con contraluz directo.",
    "Aleje la cámara si el vehículo queda cortado en los bordes.",
]


def _conf_label(conf: float) -> str:
    for threshold, label in _CONFIDENCE_LABEL:
        if conf >= threshold:
            return label
    return "muy baja"


def build_description(predictions: list[Prediction], input_type: str) -> str:
    if not predictions or predictions[0].confidence < 0.15:
        return _NO_VEHICLE_MSG

    top = predictions[0]
    body = _BODY_TYPE.get((top.brand, top.model), "vehículo de pasajeros")
    conf_pct = round(top.confidence * 100, 1)
    conf_text = _conf_label(top.confidence)
    source = "la imagen" if input_type == "image" else "la secuencia de video"

    desc = (
        f"A partir del análisis de {source}, el sistema identificó con una confianza {conf_text} "
        f"({conf_pct} %) un {top.brand} {top.model}, que corresponde a un {body}. "
    )

    if len(predictions) >= 2:
        second = predictions[1]
        desc += (
            f"Como segunda opción con menor probabilidad se obtuvo un {second.brand} {second.model} "
            f"({round(second.confidence * 100, 1)} %). "
        )

    if top.confidence < 0.5:
        desc += (
            "El nivel de confianza obtenido es moderado o bajo, por lo que se recomienda "
            "revisar las alternativas del top-3 antes de tomar una decisión definitiva."
        )
    else:
        desc += (
            f"El {top.brand} {top.model} es uno de los modelos con mayor presencia en el "
            "parque automotor colombiano, lo que favorece la precisión del clasificador."
        )

    return desc


def build_suggestions(predictions: list[Prediction]) -> list[str]:
    if not predictions or predictions[0].confidence >= 0.15:
        return []
    return _SUGGESTIONS
