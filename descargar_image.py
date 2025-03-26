import os
import json
import requests

# Nombre del archivo JSON (asegúrate de que esté en la misma carpeta que el script)
json_filename = "data/salud_bienestar.json"

# Leer el archivo JSON
with open(json_filename, "r", encoding="utf-8") as file:
    data = json.load(file)

# Carpeta donde se guardarán las imágenes
output_folder = "salud_bienestar"
os.makedirs(output_folder, exist_ok=True)

# Descargar cada imagen
for product in data:
    try:
        image_url = product.get("image_url")
        product_id = product.get("id")

        if image_url and product_id:
            # Obtener la extensión del archivo
            ext = image_url.split(".")[-1].split("?")[0]  # Manejo de parámetros en la URL
            filename = os.path.join(output_folder, f"{product_id}.{ext}")

            # Descargar la imagen
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # Verifica que la solicitud fue exitosa

            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"Imagen guardada: {filename}")

    except requests.RequestException as e:
        print(f"Error al descargar {image_url}: {e}")

print("Descarga completa.")
