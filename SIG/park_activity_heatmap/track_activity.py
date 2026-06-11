import json
import random
import requests

from shapely.geometry import Polygon
from shapely.geometry import Point

TELEGRAM_BOT_TOKEN = None
CHAT_ID = None

park = Polygon([
    (10.012967606841693, -84.22967336145524),
    (10.013118164024641, -84.22752222994986),
    (10.012600458330756, -84.2274471281018),
    (10.011961249140755, -84.22951242892367)
])

def load_keys():
    global TELEGRAM_BOT_TOKEN
    global CHAT_ID
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                TELEGRAM_BOT_TOKEN = line.strip().split("=", 1)[1]
            elif line.startswith("CHAT_ID="):
                CHAT_ID = line.strip().split("=", 1)[1]

def gen_random_point(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    while True:
        lon = random.uniform(minx, maxx)
        lat = random.uniform(miny, maxy)
        if polygon.contains(Point(lon, lat)):
            return lon, lat

def gen_random_time():
    return [
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59)
    ]

def add_minute(time_list):
    hour, minute, second = time_list

    minute += 1

    if minute >= 60:
        minute = 0
        hour = (hour + 1) % 24

    return [hour, minute, second]

def main():
    load_keys()
    puntos = []
    current_time = gen_random_time()

    for _ in range(random.randint(5, 10)):
        current_time = add_minute(current_time)

        lon, lat = gen_random_point(park)

        puntos.append({
            "latitud": lat,
            "longitud": lon,
            "hora": current_time.copy()
        })

    # Mensaje para Telegram
    message = json.dumps(puntos)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message[:4000]  # Telegram limita el tamaño del mensaje
        }
    )

if __name__ == "__main__":
    main()
