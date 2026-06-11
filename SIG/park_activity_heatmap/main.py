import json

from map_tools import coord_transformer, gen_heatmap

def main():
    # Foto de fondo
    background_path = "map1.png"

    # Límites del parque
    park = [
        (10.012967606841693, -84.22967336145524),  # A
        (10.013118164024641, -84.22752222994986),  # B
        (10.012600458330756, -84.2274471281018),   # C
        (10.011961249140755, -84.22951242892367)   # D
    ]

    new_points = input("Ingrese nuevos registros o presione ENTER para continuar: ")
    if new_points != "":
        json_points = json.loads(new_points)
        # Cargar datos previos
        try:
            with open("activity_tracked.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = []
        # Añadir nuevos registros
        datos.extend(json_points)
        # Guardar
        with open("activity_tracked.json", "w", encoding="utf-8") as f:
            json.dump(datos, f)

    with open("activity_tracked.json", "r", encoding="utf-8") as f:
        datos = json.load(f)

    points_registered = [
        coord_transformer(
            punto["longitud"],
            punto["latitud"]
        )
        for punto in datos
    ]

    gen_heatmap(background_path, points_registered)

if __name__ == "__main__":
    main()
