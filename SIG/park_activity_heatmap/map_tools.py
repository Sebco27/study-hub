import random
import numpy as np

from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter
from shapely.geometry import Point
from collections import Counter

def coord_transformer(lat, lon):
    aprox_x = (
        3037.49302 * lat
        + 358416.666 * lon
        + 30158934.9
    )

    aprox_y = (
        -317610.467 * lat
        + 12578.9379 * lon
        + 4239797.353
    )

    round_x = 5 * round(aprox_x / 5)
    round_y = 5 * round(aprox_y / 5)

    return round_x, round_y

def gen_random_point(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    while True:
        lon = random.uniform(minx, maxx)
        lat = random.uniform(miny, maxy)

        if polygon.contains(Point(lon, lat)):
            return coord_transformer(lon, lat)

def gen_heatmap(background_path, points):
    # Ruta de la imagen de fondo
    background = plt.imread(background_path)

    # Imagen de fondo
    background = plt.imread(background_path)
    height, width = background.shape[:2]

    # Matriz vacía
    heatmap = np.zeros((height, width))

    # Registrar intensidad
    counts = Counter(points)
    heat_points = [(x, y, count) for (x, y), count in counts.items()]
    for x, y, heat in heat_points:
        heatmap[y, x] = heat

    # Suavizar para generar áreas de calor
    heatmap = gaussian_filter(heatmap, sigma=25)

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.imshow(background)
    ax.imshow(
        heatmap,
        cmap="jet",
        alpha=0.25
    )

    # Mostrar mapa de calor
    ax.axis("off")
    plt.show()
