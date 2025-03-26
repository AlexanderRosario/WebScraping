
# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
import os
# Import to format the JSON responses
# ==============================
import json
# Copy and paste your API environment variable
# =============================================
# CLOUDINARY_URL=cloudinary://358361244321745:mx_ndSL9U44IrdO-T6KSfkEkSUA@ds49swxwx
cloudinary_url = os.getenv("CLOUDINARY_URL")
# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================


if not cloudinary_url:
    raise ValueError("❌ ERROR: CLOUDINARY_URL no está definida. Verifica tu archivo .env.")

config = cloudinary.config(secure=True)
# Log the configuration
# ==============================
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")



# Ruta de la carpeta con imágenes
folder_path = r"C:\Users\juniora\Documents\Scraping\alimentacion"

# Verificar si la carpeta existe
if not os.path.exists(folder_path):
    print(f"❌ Error: La carpeta '{folder_path}' no existe.")
    exit()


# Obtener la lista de archivos en la carpeta
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Verificar si hay imágenes en la carpeta
if not image_files:
    print("❌ No se encontraron imágenes en la carpeta.")
    exit()

# Función para subir una imagen a Cloudinary
def upload_image(image_path, public_id):
    try:
        response = cloudinary.uploader.upload(image_path, public_id=public_id, unique_filename=False, overwrite=True)
        image_url = response.get("secure_url", "")
        print(f"✅ Imagen subida: {image_path} -> {image_url}")
    except Exception as e:
        print(f"❌ Error al subir {image_path}: {e}")

# Subir todas las imágenes de la carpeta
for idx, image_file in enumerate(image_files):
    image_path = os.path.join(folder_path, image_file)
    public_id = f"producto_{idx + 1}"  # Puedes cambiar la lógica del ID
    upload_image(image_path, public_id)