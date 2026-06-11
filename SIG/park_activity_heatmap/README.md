# Mapa de calor de actividad en parque

Este proyecto genera un mapa de calor a partir de registros de actividad (coordenadas GPS) dentro de un parque delimitado. Los datos pueden enviarse mediante un bot de Telegram y se almacenan en un archivo JSON para luego visualizarse como un mapa de calor superpuesto en una imagen del parque.

## Características

- Generación de puntos aleatorios dentro de un polígono que representa el parque.
- Envío de los puntos generados a un chat de Telegram.
- Transformación de coordenadas geográficas a píxeles en una imagen de fondo.
- Acumulación de registros en `activity_tracked.json`.
- Generación de un mapa de calor con suavizado gaussiano.

## Requisitos

- Python 3.7 o superior.
- Las dependencias listadas en `requirements.txt`.

## Instalación

1. Clona o descarga este repositorio.
2. (Opcional) Crea y activa un entorno virtual.
3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración del bot de Telegram (solo admins)

Si deseas usar el script `track_activity.py` para recibir datos automáticamente, necesitas un bot de Telegram.

1. Crea un bot con [@BotFather](https://t.me/BotFather) y obtén su token.
2. Obtén tu `chat_id` (puedes usar el bot `@userinfobot` o enviar un mensaje a tu bot y consultar `https://api.telegram.org/bot<TOKEN>/getUpdates`).
3. Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```
TELEGRAM_BOT_TOKEN=tu_token
CHAT_ID=tu_chat_id
```

## Archivos necesarios

- `map1.png`: imagen de fondo del parque (debe coincidir visualmente con las coordenadas transformadas).
- `activity_tracked.json`: en caso de no existir, se creará automáticamente al recibir el primer registro.

## Uso

### 1. Generar y enviar datos simulados (opcional)

Ejecuta `track_activity.py` para generar entre 5 y 10 puntos aleatorios dentro del parque, con tiempos simulados, y enviarlos por Telegram:

```bash
python track_activity.py
```

El mensaje enviado contiene un JSON con la lista de registros. Cópialo para pegarlo en el siguiente paso.

### 2. Agregar registros y generar el mapa de calor

Ejecuta `main.py`. Si pegas un JSON válido (como el enviado por Telegram) y presionas Enter, los nuevos puntos se agregarán al archivo `activity_tracked.json`. Luego, el programa generará y mostrará el mapa de calor.

```bash
python main.py
```

Al ejecutarlo:

- Puedes presionar Enter para no ingresar datos nuevos.
- El programa cargará todos los puntos acumulados en `activity_tracked.json`.
- Transformará las coordenadas geográficas a píxeles usando la función `coord_transformer`.
- Generará un mapa de calor (con `gaussian_filter`) y lo mostrará superpuesto en `map1.png`.

## Estructura del proyecto

```
├── main.py                  # Punto de entrada: carga datos y genera heatmap
├── map_tools.py             # Transformación de coordenadas y generación del heatmap
├── track_activity.py        # Genera puntos aleatorios y los envía por Telegram
├── activity_tracked.json    # Almacenamiento persistente de registros (se crea al usar)
├── map1.png                 # Imagen de fondo del parque
├── .env                     # Variables de entorno para Telegram (no incluido en el repo)
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```

---

<div align="center">
<a href="https://www.tec.ac.cr/"><img src="https://www.tec.ac.cr/themes/custom/tecnologico/logo.svg" width="300" style="vertical-align: middle;"/></a>
</div>