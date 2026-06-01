from shapely.geometry import Polygon, polygon
from map_tools import gen_random_point, gen_heatmap

def main():
    # Foto de fondo
    background_path = "map.png"

    # Límites del parque
    park = Polygon([
        (10.012967606841693, -84.22967336145524),  # A
        (10.013118164024641, -84.22752222994986),  # D
        (10.012600458330756, -84.2274471281018),   # E
        (10.011961249140755, -84.22951242892367)   # C
    ])

    # Lista de puntos a simular
    points_registered = []

    for _ in range(5): # Simulación de puntos
        points_registered = points_registered + [gen_random_point(park) for _ in range(15)]

    gen_heatmap(background_path, points_registered)

if __name__ == "__main__":
    main()
