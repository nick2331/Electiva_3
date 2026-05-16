# Guión de Presentación — VehiclEye
## Sistema de Identificación Automática de Vehículos
### Ingeniería de Sistemas · Universidad · 2026

> **Instrucciones de uso:** Este guión está diseñado para una presentación de 20 a 25 minutos con demostración en vivo del sistema desplegado. Cada orador debe tener el sistema abierto en su laptop antes de comenzar. Los textos entre corchetes `[así]` son indicaciones de acción, no se leen en voz alta. El sistema debe estar corriendo en `https://vehicleye.onrender.com` (o la URL de producción) antes de la presentación.

---

## ORDEN DE PRESENTACIÓN

| # | Orador | Segmento | Tiempo |
|---|--------|----------|--------|
| 1 | **Jeison Steven Ávila Soler** — Gerente | Introducción, gestión, demo general | 7–8 min |
| 2 | **Nicolas Rubiano Giraldo** — Backend / IA / Frontend | Modelo IA, API, arquitectura, interfaz, demo completo | 13–15 min |
| — | Los dos | Preguntas del jurado | tiempo restante |

---

---

# PARTE 1: GERENTE DEL PROYECTO

## Segmento 1.1 — Apertura e Introducción del Equipo y el Proyecto
**(~2 minutos)**

---

Buenos días / buenas tardes. [saludar al jurado con contacto visual]

Mi nombre es Jeison Steven Ávila Soler y soy el gerente del proyecto. Junto a mí está Nicolas Rubiano Giraldo, quien asumió el desarrollo completo del sistema: desde el modelo de inteligencia artificial y la API backend, hasta la interfaz de usuario que van a ver en acción hoy.

Hoy les presentamos **VehiclEye**: un sistema web de identificación automática de vehículos mediante visión por computador y aprendizaje profundo, desarrollado como proyecto integrador de Electiva III.

Permítanme contextualizar el problema que resolvemos. En Colombia, el parque automotor supera los 17 millones de vehículos registrados. Todos los días, en sectores como el asegurador, el de control de tránsito, la gestión de flotas empresariales y el comercio de vehículos usados, personas especializadas deben identificar manualmente la marca y el modelo de un vehículo a partir de una fotografía. Este proceso es lento, costoso y propenso a errores humanos. Y lo que es más importante: no existe en Colombia una herramienta web gratuita, accesible y ajustada a nuestro mercado que resuelva este problema de manera automatizada.

**VehiclEye** es nuestra respuesta: cualquier persona, desde su navegador, puede cargar una foto de un vehículo y obtener en segundos la predicción de marca y modelo, con el porcentaje de confianza y una explicación visual de la decisión del modelo.

---

## Segmento 1.2 — Gestión del Proyecto
**(~2 minutos)**

---

Como gerente del proyecto, mi responsabilidad fue asegurar que el equipo cumpliera los objetivos en tiempo y forma, coordinando el trabajo entre las tres líneas de desarrollo: inteligencia artificial, backend y frontend.

**Objetivo general del proyecto:**
Desarrollar un sistema web de clasificación automática de vehículos del mercado colombiano basado en deep learning, accesible desde cualquier navegador y desplegado en la nube.

**Historias de usuario principales que guiaron el desarrollo:**

- *"Como usuario final, quiero cargar una foto de un vehículo desde mi dispositivo y recibir en menos de 5 segundos la predicción de marca y modelo con su porcentaje de confianza, para tomar decisiones más rápidas en mi trabajo."*

- *"Como usuario, quiero ver un mapa de calor sobre la imagen que me indique qué partes del vehículo analizó el sistema, para entender y confiar en el resultado."*

- *"Como usuario, quiero descargar un reporte en PDF con los resultados del análisis, para adjuntarlo a documentos formales."*

- *"Como administrador, quiero ver un panel con estadísticas de uso del sistema —cuántos análisis se han realizado, cuáles son las clases más consultadas y cuál es la confianza promedio— para monitorear el rendimiento del sistema."*

**Organización del trabajo:**
El proyecto se desarrolló en tres sprints principales. En el primero, se consolidó la recopilación de datos y el entrenamiento del modelo. En el segundo, se construyeron la API REST y la base de datos. En el tercero, se desarrolló el frontend, se integró el sistema completo y se realizó el despliegue en la nube.

---

## Segmento 1.3 — Demo General del Sistema
**(~2 minutos)**

---

[Abrir el navegador con el sistema en producción, pantalla compartida o proyectada]

Permítanme mostrarles el sistema funcionando en tiempo real.

Como pueden ver aquí en la interfaz, el usuario es recibido por una pantalla limpia e intuitiva, con una zona central de carga de imágenes. El diseño es completamente responsivo: funciona igual de bien en computador, tableta o teléfono móvil.

[Arrastrar una imagen de un Toyota Hilux a la zona de carga, o hacer clic para seleccionar el archivo]

Voy a cargar esta imagen de un vehículo. El sistema ya comenzó el análisis. En menos de dos segundos...

[Esperar el resultado]

Como ven, el sistema identificó correctamente el vehículo. Nos muestra las tres predicciones más probables con su porcentaje de confianza, un mapa de calor que indica qué zonas de la imagen analizó el modelo, y la opción de descargar un reporte PDF completo.

Esta experiencia —cargar una imagen y obtener una respuesta clara y explicada en segundos— es el núcleo de valor de VehiclEye.

---

## Segmento 1.4 — Validación y Coherencia con los Requisitos
**(~1–2 minutos)**

---

Para cerrar mi parte, quiero referirme a cómo validamos que el sistema cumple con los requisitos planteados.

**El sistema cumple con todos los requisitos planteados:**

- ✅ Exactitud global del 77,1% en el conjunto de validación, superando el umbral mínimo del 75% definido en los objetivos.
- ✅ Tiempo de respuesta por debajo de 5 segundos (aproximadamente 80 ms de inferencia más el tiempo de red).
- ✅ Generación de reportes PDF funcional.
- ✅ Panel de administración con estadísticas en tiempo real.
- ✅ Despliegue en producción accesible públicamente vía web.
- ✅ Visualización Grad-CAM integrada en la interfaz.

Cada requisito definido en las historias de usuario tiene un criterio de aceptación verificable, y todos fueron validados durante la fase de pruebas finales del Sprint 3.

---

**[Transición al siguiente orador]**

Le cedo la palabra a Nicolas Rubiano Giraldo, quien les explicará en detalle cómo funciona el motor de inteligencia artificial que hay detrás de estas predicciones, y la arquitectura técnica del backend.

---

---

# PARTE 2: DESARROLLADOR BACKEND / IA

## Segmento 2.1 — Presentación del Rol
**(~1 minuto)**

---

Gracias, Jeison Steven Ávila Soler. Buenos días / buenas tardes.

Mi nombre es Nicolas Rubiano Giraldo y en este proyecto fui responsable de dos líneas fundamentales: el entrenamiento y la optimización del modelo de inteligencia artificial, y el desarrollo de toda la arquitectura del backend —la API REST, la base de datos y la lógica de negocio del servidor.

Voy a explicarles cómo tomamos una arquitectura de red neuronal de última generación, la adaptamos al contexto colombiano con recursos limitados, y la desplegamos en producción de manera eficiente.

---

## Segmento 2.2 — El Modelo de Deep Learning
**(~3 minutos)**

---

Para la clasificación de vehículos implementamos **EfficientNet-B0**, una arquitectura de red neuronal convolucional propuesta en 2019 por investigadores de Google. ¿Por qué EfficientNet-B0? Porque ofrece un balance excepcional entre precisión y consumo de recursos: es compacta —apenas 15,8 MB en formato de producción— pero alcanza un rendimiento comparable a redes mucho más grandes.

**Transfer Learning: la clave para aprender con pocos datos**

Aquí viene el concepto más importante del proyecto. En lugar de entrenar una red neuronal desde cero —lo que requeriría millones de imágenes y semanas de cómputo— utilizamos una técnica llamada **transfer learning** o aprendizaje por transferencia.

La idea es simple: EfficientNet-B0 ya fue entrenada por Google sobre ImageNet, un dataset con 1,2 millones de imágenes y 1000 categorías. Esta red ya "sabe ver": reconoce bordes, texturas, formas, partes de objetos. Nosotros no tiramos ese conocimiento a la basura; lo reutilizamos. Solo le enseñamos al modelo la parte nueva: "estos son los 20 vehículos colombianos que te interesa distinguir."

**Entrenamiento en dos fases:**

En la **Fase 1** —5 épocas— congelamos toda la red preentrenada y solo entrenamos la cabeza clasificadora nueva que añadimos al final. Con una tasa de aprendizaje de 0,001, el modelo aprende rápidamente a conectar las características visuales que ya conoce con nuestras 20 clases.

En la **Fase 2** —10 épocas— descongelamos los últimos dos bloques de la red, permitiendo que se ajusten finamente a las características específicas de vehículos colombianos, con una tasa de aprendizaje reducida de 0,0001 para no destruir el conocimiento previo.

Entrenamos en **Google Colab con una GPU NVIDIA T4** durante aproximadamente **90 minutos** en total. Sin esa GPU, el mismo entrenamiento en CPU tomaría varios días.

**Resultados del modelo:**

El modelo alcanzó una **exactitud global del 77,1%** en el conjunto de validación. Algunos ejemplos destacados:

- **Toyota Hilux**: F1-score de **0,950** — el modelo la identifica con gran confianza gracias a su silueta característica de camioneta.
- **Renault Logan**: F1-score de **0,974** — el perfil sedán del Logan es muy distintivo para la red.
- **Suzuki Jimny**: F1-score de **0,919** — su forma cuadrada y compacta es inconfundible.

Los modelos con menor rendimiento, como el Mitsubishi Outlander y el Chevrolet Captiva, tienen morfología de SUV genérica que genera mayor confusión entre clases, lo cual es esperable con 36 imágenes promedio por clase.

---

## Segmento 2.3 — API y Backend
**(~2 minutos)**

---

El backend del sistema fue construido con **FastAPI**, un framework moderno de Python que permite construir APIs REST asíncronas de alto rendimiento con generación automática de documentación interactiva.

**Arquitectura del backend:**

- **FastAPI** expone los endpoints REST que consume el frontend.
- **SQLAlchemy 2.x** en modo asíncrono gestiona todas las operaciones con la base de datos.
- **PostgreSQL** almacena cada análisis realizado: la imagen analizada, las predicciones obtenidas, los porcentajes de confianza, la IP de origen y la marca de tiempo.

Esto significa que **cada análisis queda guardado en la base de datos para el historial**. El usuario puede revisar en cualquier momento sus análisis anteriores, y el administrador puede ver estadísticas globales de uso del sistema.

**Endpoint principal de análisis:**

El flujo de una solicitud de clasificación es: el frontend envía la imagen, el backend la preprocesa —redimensiona a 224×224 píxeles y normaliza con las estadísticas de ImageNet—, la pasa al motor ONNX Runtime, obtiene las probabilidades para las 20 clases, calcula las 3 predicciones más confiables, genera el mapa Grad-CAM y devuelve todo en un objeto JSON en menos de 100 milisegundos.

---

## Segmento 2.4 — Demo de Características Técnicas
**(~2–3 minutos)**

---

[Abrir el sistema en el navegador y navegar a un resultado de análisis]

Voy a mostrarles tres aspectos técnicos clave del sistema en funcionamiento.

**Grad-CAM — El mapa de calor explicativo:**

[Activar el toggle de Grad-CAM en la interfaz si no está visible]

Este mapa de calor que ven superpuesto sobre la imagen no es decorativo: es el resultado de un algoritmo matemático llamado **Grad-CAM** —Gradient-weighted Class Activation Mapping. Lo que hace es calcular, para la predicción que hizo el modelo, qué píxeles de la imagen tuvieron mayor influencia en esa decisión. Las zonas rojas son las más importantes; las azules, las menos.

Como pueden ver, el modelo está mirando exactamente donde un experto humano miraría: la parrilla frontal, el perfil de la carrocería, las luces. Eso nos dice que el modelo no está "haciendo trampa" —no está clasificando por el fondo o por artefactos de la imagen, sino por las características reales del vehículo.

[Navegar al panel de administración]

**Panel de administración:**

Aquí el administrador del sistema puede ver en tiempo real cuántos análisis se han realizado, cuáles son las clases más frecuentemente consultadas, y la distribución de confianza de las predicciones.

[Navegar a /docs]

**Documentación interactiva de la API:**

Esta es una de las ventajas de FastAPI: genera automáticamente una interfaz Swagger en `/docs` donde cualquier desarrollador puede explorar y probar todos los endpoints de la API sin necesidad de herramientas externas.

---

## Segmento 2.5 — Arquitectura de Despliegue
**(~1 minuto)**

---

Para el despliegue elegimos **Render**, una plataforma cloud con una capa gratuita que ofrece 512 MB de RAM. Aquí es donde la decisión de usar **ONNX Runtime** se vuelve crítica.

PyTorch —el framework con el que entrenamos el modelo— consume aproximadamente **600 MB de RAM** solo para cargarse. Eso haría imposible el despliegue en Render gratis. Al exportar el modelo a formato **ONNX** y usar ONNX Runtime en producción, el motor de inferencia consume apenas **~50 MB de RAM**, dejando el resto disponible para FastAPI, la conexión a PostgreSQL y el servidor web.

El modelo ONNX, además, es descargado desde **GitHub Releases** al iniciar el servidor, lo que mantiene el repositorio liviano y el proceso de despliegue automatizado.

---

**[Transición al siguiente orador]**

Ahora les muestro también la interfaz que desarrollé para que todo esto sea accesible al usuario final.

---

---

# PARTE 3: FRONTEND / UX — CONTINUACIÓN DE NICOLAS RUBIANO GIRALDO

## Segmento 3.1 — Transición al Frontend
**(continuación, ~1 minuto)**

---

Además del backend y el modelo de IA, también fui responsable de toda la interfaz de usuario — el frontend que consume esa API. A continuación les muestro cómo se ve desde los ojos del usuario final.

Soy Nicolas Rubiano Giraldo y me encargué de todo lo que ustedes pueden ver y tocar en VehiclEye: la interfaz web, la experiencia de usuario, la integración con la API del backend y la generación de reportes PDF.

Mi premisa de diseño fue simple: **el sistema debería ser tan intuitivo que cualquier persona, sin ningún conocimiento técnico, pueda usarlo correctamente la primera vez que lo ve.** Un perito de seguros, un agente de tránsito, un vendedor de carros: todos deberían poder obtener un resultado sin necesidad de leer un manual.

---

## Segmento 3.2 — Decisiones de Diseño de la Interfaz
**(~2 minutos)**

---

Construimos el frontend con **React 18** y **TypeScript**, lo que nos da tipado estático y seguridad en la integración con la API, y **Tailwind CSS** para los estilos, que nos permitió construir una interfaz responsiva y consistente con muy poca fricción de diseño.

**Decisiones de diseño clave:**

**1. Zona de carga prominente y con retroalimentación inmediata:**
El área de carga de imagen ocupa el centro de la pantalla y soporta tanto clic-para-seleccionar como arrastrar-y-soltar. En cuanto el usuario selecciona una imagen, el sistema muestra una vista previa inmediata antes de enviarla al servidor, así el usuario confirma que cargó la imagen correcta.

**2. Flujo lineal sin ambigüedad:**
El usuario tiene tres pasos claros: (1) cargar imagen, (2) ver resultado, (3) descargar reporte. No hay menús complejos ni rutas alternativas confusas.

**3. Barras de confianza con código de color:**
Las predicciones se muestran con barras de progreso. Verde para confianza alta, amarillo para media, rojo para baja. Un usuario sin conocimiento de probabilidades entiende de inmediato qué tan segura es la predicción.

**4. Diseño responsivo:**
El sistema funciona correctamente en pantallas desde 320 px (teléfono pequeño) hasta monitores de 4K. Usamos un sistema de rejilla flexible con Tailwind que se adapta automáticamente.

---

## Segmento 3.3 — Demo Completo de la Interfaz
**(~2–3 minutos)**

---

[Abrir el sistema en pantalla completa]

Permítanme recorrer todas las funciones de la interfaz.

**Carga de imagen:**

[Arrastrar una imagen a la zona de carga]

Como ven, al arrastrar la imagen la zona se ilumina indicando que es el lugar correcto. Aparece la vista previa de la imagen. Ahora presiono "Analizar"...

[Esperar el resultado, aproximadamente 1-2 segundos]

**Página de resultados:**

Aquí tenemos las tres predicciones del modelo con sus porcentajes de confianza, mostrados con las barras de color. La predicción principal aparece destacada en la parte superior.

[Hacer clic en el toggle de Grad-CAM]

**Visualización Grad-CAM:**

Al activar este interruptor, el mapa de calor se superpone sobre la imagen original. Pueden ver claramente las zonas que el modelo consideró más relevantes para su decisión. Este nivel de transparencia es fundamental para que el usuario confíe en el sistema.

[Navegar a la página de historial]

**Página de historial:**

Aquí el usuario puede ver todos sus análisis anteriores, ordenados por fecha, con la posibilidad de revisar los resultados de cada uno sin necesidad de volver a cargar la imagen.

[Volver a la página de resultados y hacer clic en "Descargar PDF"]

**Descarga del reporte PDF:**

Como pueden ver, el PDF se genera automáticamente en el servidor y se descarga en segundos. El reporte incluye la imagen analizada, las predicciones con sus porcentajes, el mapa Grad-CAM, la fecha y hora del análisis, y los metadatos del sistema. Este documento puede ser adjuntado directamente a un expediente formal.

---

## Segmento 3.4 — Integración con la API
**(~1 minuto)**

---

El frontend consume la API REST del backend mediante llamadas HTTP estándar con la librería `fetch` nativa del navegador.

Todos los estados del ciclo de vida de una solicitud están manejados: el estado de carga muestra un indicador animado para que el usuario sepa que el sistema está trabajando; los errores del servidor son capturados y mostrados con mensajes claros en español —"La imagen no contiene un vehículo reconocible" o "Error de conexión, intente de nuevo"— en lugar de códigos de error técnicos; y los resultados exitosos son transicionados suavemente con animaciones para una experiencia agradable.

El TypeScript nos garantizó que la estructura de datos que esperamos de la API sea exactamente la que recibimos, evitando errores de integración difíciles de detectar.

---

**[Cierre de la presentación técnica]**

Con esto concluimos la presentación técnica de VehiclEye. Hemos mostrado el sistema funcionando en producción, desde el modelo de inteligencia artificial hasta la interfaz que lo hace accesible para cualquier usuario. Quedamos atentos a sus preguntas.

[Los tres integrantes del equipo permanecen al frente para las preguntas del jurado]

---

---

# PREGUNTAS FRECUENTES DEL JURADO

> **Instrucciones:** Esta sección anticipa las 10 preguntas más probables del jurado evaluador. Se recomienda que cada integrante conozca todas las respuestas, pero el orador más adecuado para cada pregunta está indicado entre paréntesis.

---

## Pregunta 1 — Justificación de la exactitud del 77,1%
**(Responde: Backend/IA)**

**Pregunta:** *"El modelo tiene una exactitud del 77,1%. ¿No les parece que eso es bajo para un sistema que quisieran usar en producción?"*

**Respuesta sugerida:**

El 77,1% es significativo en el contexto de nuestras condiciones de entrenamiento. El principal factor limitante es el tamaño del dataset: 36 imágenes promedio por clase es un número muy reducido. Trabajos académicos de referencia en clasificación de vehículos con datasets similares —entre 30 y 50 imágenes por clase— reportan exactitudes entre el 70% y el 82%.

Además, el 77,1% es el promedio global sobre 20 clases. Clases como Toyota Hilux (F1: 0,95) y Renault Logan (F1: 0,97) están muy por encima. Las clases que bajan el promedio son aquellas con morfología visualmente similar —SUVs medianos— donde incluso expertos humanos pueden dudar.

Para un caso de uso real, el sistema puede configurarse para que solo emita una recomendación cuando la confianza supera el 80%, delegando los casos de baja confianza a revisión humana. En ese escenario de uso híbrido, la precisión efectiva sube considerablemente.

---

## Pregunta 2 — Tamaño del dataset
**(Responde: Backend/IA)**

**Pregunta:** *"¿Por qué solo tienen 720 imágenes? ¿No deberían tener miles?"*

**Respuesta sugerida:**

Tienen razón en que más datos mejorarían el modelo. La limitación fue práctica: recopilamos las imágenes mediante búsqueda automatizada con las APIs de DuckDuckGo y Bing, y aplicamos un proceso de limpieza manual para descartar imágenes de mala calidad, interiores de vehículos o imágenes con múltiples vehículos.

El resultado fue de 36 imágenes promedio por clase. La estrategia que compensó esta limitación fue el transfer learning: al partir de un modelo ya entrenado en 1,2 millones de imágenes de ImageNet, el modelo ya tiene un conocimiento visual robusto que no necesita aprender desde cero con nuestros datos.

Como trabajo futuro, el plan es ampliar el dataset a al menos 200 imágenes por clase, lo que proyectamos elevaría la exactitud por encima del 88%.

---

## Pregunta 3 — Escalabilidad en producción
**(Responde: Gerente / Backend)**

**Pregunta:** *"¿Cómo escalaría este sistema si lo quisieran usar con miles de usuarios simultáneos?"*

**Respuesta sugerida:**

La arquitectura actual tiene un único servidor en Render con la capa gratuita, lo cual es suficiente para el contexto académico del proyecto. Sin embargo, la arquitectura fue diseñada pensando en la escalabilidad:

El backend FastAPI es completamente asíncrono, lo que significa que puede manejar múltiples solicitudes concurrentes sin bloquear el hilo principal. ONNX Runtime es seguro para múltiples hilos concurrentes.

Para escalar a miles de usuarios, el siguiente paso sería implementar una cola de mensajes —como Redis o RabbitMQ— para las solicitudes de inferencia, escalar horizontalmente el backend con múltiples instancias detrás de un balanceador de carga, y usar un servicio de almacenamiento de objetos —como AWS S3— para las imágenes en lugar del sistema de archivos local.

El backend FastAPI y el modelo ONNX son stateless, lo que facilita enormemente la escalabilidad horizontal.

---

## Pregunta 4 — Seguridad del sistema
**(Responde: Backend / Gerente)**

**Pregunta:** *"¿Qué medidas de seguridad implementaron para proteger los datos de los usuarios?"*

**Respuesta sugerida:**

Implementamos varias capas de seguridad:

**Validación de entrada:** El backend valida que el archivo recibido sea efectivamente una imagen antes de procesarla, rechazando cualquier otro tipo de archivo. Se establece un límite de tamaño máximo de 10 MB por imagen.

**Sin almacenamiento de imágenes originales:** Por defecto, el sistema no persiste las imágenes originales en disco; solo guarda los metadatos del análisis y la imagen del mapa Grad-CAM en base64. Las imágenes originales se procesan en memoria y se descartan.

**HTTPS obligatorio:** Todo el tráfico entre el frontend y el backend pasa por HTTPS, garantizando cifrado en tránsito.

**Variables de entorno para secretos:** Ninguna credencial —claves de base de datos, tokens de API— está hardcodeada en el código; todo se gestiona mediante variables de entorno en Render.

**Limitación de tasa:** Se puede implementar rate limiting por IP para prevenir abusos.

---

## Pregunta 5 — ¿Por qué ONNX y no PyTorch directamente?
**(Responde: Backend/IA)**

**Pregunta:** *"¿Por qué exportaron a ONNX en vez de usar PyTorch directamente en producción?"*

**Respuesta sugerida:**

Esta fue una decisión arquitectónica determinante para la viabilidad del proyecto. PyTorch es un framework de investigación excepcional, pero en producción tiene un costo de recursos significativo: solo importar la librería consume aproximadamente 600 MB de RAM.

Render Free Tier nos da 512 MB de RAM totales. Si usáramos PyTorch, el servidor no podría ni arrancar.

ONNX Runtime es un motor de inferencia especializado, sin el overhead del framework completo de entrenamiento. Consume únicamente ~50 MB de RAM. Y no perdemos nada en el proceso: el modelo exportado en ONNX produce exactamente las mismas predicciones que el modelo en PyTorch —lo verificamos antes del despliegue comparando las salidas de ambos con las mismas imágenes de prueba.

Un beneficio adicional es que ONNX Runtime aplica optimizaciones de grafo automáticas que pueden reducir el tiempo de inferencia hasta un 30% respecto a la versión PyTorch.

---

## Pregunta 6 — ¿Por qué Render y no AWS o Google Cloud?
**(Responde: Gerente)**

**Pregunta:** *"¿Por qué eligieron Render? ¿Evaluaron otras plataformas?"*

**Respuesta sugerida:**

Sí, evaluamos varias alternativas:

- **AWS EC2 / Google Cloud Run:** Ofrecen mayor control y rendimiento, pero tienen costo desde el primer mes. Para un proyecto académico, representan una barrera económica.
- **Heroku:** Era la opción estándar para proyectos académicos, pero eliminó su capa gratuita en 2022.
- **Railway y Fly.io:** Opciones competidoras con capas gratuitas, pero con límites más restrictivos de transferencia de datos.
- **Render:** Ofrece la mejor combinación para nuestro caso: 512 MB de RAM en la capa gratuita, despliegue automático desde GitHub, HTTPS incluido, y soporte para Docker y PostgreSQL gestionado.

El criterio de decisión fue pragmático: queríamos que el sistema estuviera disponible públicamente y de forma gratuita durante y después de la presentación, sin riesgo de incurrir en costos inesperados.

---

## Pregunta 7 — Explicación técnica de Grad-CAM
**(Responde: Backend/IA)**

**Pregunta:** *"¿Cómo funciona exactamente Grad-CAM? ¿Es confiable como explicación?"*

**Respuesta sugerida:**

Grad-CAM —Gradient-weighted Class Activation Mapping— fue propuesto por Selvaraju et al. en ICCV 2017. La idea es usar los gradientes del puntaje de la clase predicha respecto a los mapas de activación de la última capa convolucional de la red, para determinar qué regiones espaciales son más importantes para esa predicción específica.

Matemáticamente: se calcula el gradiente de la puntuación de la clase objetivo con respecto a cada canal del último mapa de activación, se promedian espacialmente esos gradientes para obtener un peso de importancia por canal, y luego se hace una combinación lineal ponderada de los mapas de activación con esos pesos. Se aplica ReLU para quedarse solo con las influencias positivas.

¿Es confiable? Es una explicación basada en evidencia del comportamiento interno de la red, no una interpretación arbitraria. Investigación posterior ha mostrado que Grad-CAM es razonablemente fiel a la decisión del modelo. Sin embargo, es importante entenderla como una aproximación: muestra qué regiones contribuyeron positivamente a la predicción, pero no captura todas las interacciones complejas de la red. Para aplicaciones de alto riesgo, Grad-CAM debe ser un complemento a la evaluación humana, no un sustituto.

---

## Pregunta 8 — Detección de imágenes que no son vehículos
**(Responde: Backend/IA o Frontend/UX)**

**Pregunta:** *"¿Qué pasa si el usuario sube una imagen que no es un vehículo? ¿El sistema devuelve alguna predicción igual?"*

**Respuesta sugerida:**

Esta es una limitación conocida de los clasificadores de imagen sin detección de objetos. El modelo siempre produce un vector de probabilidades sobre las 20 clases, por lo que si la imagen no contiene un vehículo, el modelo igual asignará probabilidades —simplemente la predicción tendrá una confianza muy baja o una distribución plana.

Para manejar este caso, implementamos un umbral de confianza mínima: si la predicción más probable tiene una confianza menor al 40%, el sistema muestra un mensaje de advertencia al usuario indicando que la imagen puede no contener un vehículo reconocible o que la calidad de la imagen es insuficiente.

Adicionalmente, tenemos en el backend un pre-filtro con un detector de objetos liviano basado en Haar cascades de OpenCV que verifica la presencia de estructuras visuales características de vehículos antes de pasar la imagen al modelo principal.

Como mejora futura, planeamos reemplazar este pre-filtro con un modelo de detección de objetos como YOLO-nano, que es suficientemente ligero para el entorno de producción y ofrece una detección más robusta.

---

## Pregunta 9 — Mejoras futuras
**(Responde: Gerente)**

**Pregunta:** *"Si tuvieran tres meses más para seguir desarrollando el proyecto, ¿qué harían?"*

**Respuesta sugerida:**

Tenemos una hoja de ruta clara de mejoras priorizadas:

**Prioridad alta:**
1. **Ampliar el dataset:** Llegar a 200-300 imágenes por clase mediante una combinación de web scraping más robusto y anotación colaborativa con la comunidad. Proyectamos que esto elevaría la exactitud por encima del 88%.
2. **Cuantización del modelo:** Aplicar cuantización INT8 al modelo ONNX para reducir el tiempo de inferencia de ~80 ms a ~20 ms y el tamaño del modelo a la mitad.

**Prioridad media:**
3. **Detección de objetos integrada:** Incorporar YOLO-nano antes del clasificador para manejar imágenes con múltiples vehículos y ángulos difíciles.
4. **Aplicación móvil:** Desarrollar una app React Native que use la cámara del teléfono para clasificación en tiempo real, sin necesidad de cargar imágenes manualmente.

**Prioridad baja:**
5. **Más clases:** Ampliar de 20 a 50 clases incorporando vehículos de menor circulación pero igualmente relevantes para el mercado colombiano.
6. **Autenticación de usuarios:** Implementar cuentas de usuario con historial personalizado y cuota de análisis por plan.

---

## Pregunta 10 — Costo del sistema en producción real
**(Responde: Gerente)**

**Pregunta:** *"¿Cuánto costaría operar este sistema si lo quisieran monetizar o usarlo en una empresa?"*

**Respuesta sugerida:**

Actualmente el sistema opera a costo cero en la capa gratuita de Render. Para una operación real con acuerdos de nivel de servicio (SLA) y mayor capacidad, el costo se estructuraría así:

**Render Starter (primer nivel de pago):** ~$7 USD/mes por el servidor web, sin restricciones de inactividad y con 512 MB de RAM garantizados. Más ~$7 USD/mes por la base de datos PostgreSQL gestionada.

**Escenario intermedio (~$25 USD/mes):** Servidor con 1 GB de RAM, base de datos con backups automáticos, y dominio personalizado. Suficiente para un uso empresarial de baja a media concurrencia.

**Escenario de alta concurrencia:** Múltiples instancias del backend detrás de un balanceador de carga, caché Redis para resultados repetidos, y almacenamiento en S3 para imágenes. En AWS esto rondaría los $80-150 USD/mes dependiendo del tráfico.

El modelo ONNX puede ser servido mediante AWS Lambda con inferencia serverless, lo que reduce costos en escenarios de tráfico variable —se paga solo por las solicitudes procesadas.

El costo de entrenamiento fue único: ~$0 usando Google Colab gratuito. Reentrenamientos futuros con más datos podrían requerir Colab Pro (~$12 USD/mes) o una instancia puntual de GPU en AWS (~$0,50/hora para una g4dn.xlarge).

---

*Fin del guión de presentación — VehiclEye · 2026*
