import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Configuración de opciones de Edge
options = Options()
options.add_argument("--start-maximized")  # Abrir el navegador en pantalla completa
options.add_argument("--headless")  # Opcional: ejecutar en modo sin interfaz gráfica (headless)

# Inicializar el driver de Edge
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# URL de la página a scrapear
base_url = "https://www.sirena.do/products/category/ropa?page={}&limit=45&sort=1"
# base_url = "https://www.sirena.do/products/category/limpieza-?page={}&limit=45&sort=1"
# base_url = "https://www.sirena.do/products/category/cuidado-personal-y-belleza?page={}&limit=45&sort=1"
# base_url = "https://www.sirena.do/products/category/salud-bienestar?page={}&limit=45&sort=1"
# base_url = "https://www.sirena.do/products/category/frutas-y-vegetales?page={}&limit=45&sort=1"
# base_url = "https://www.sirena.do/products/category/hogar-y-electrodomesticos?page={}&limit=45&sort=1"
# base_url = "https://www.sirena.do/products/category/bebidas?page={}&limit=45&sort=1"
# base_url = "https://www.sirena.do/products/category/alimentacion?page={}&limit=15&sort=1"

# Función para extraer productos de una página
def extract_products(soup):
    productos = []
    for item in soup.find_all("div", class_="item-product"):
        product_id = item.get("id", "")
        
        # Extraer el título y URL del producto
        title_element = item.select_one(".item-product-title a")
        title = title_element.text.strip() if title_element else "N/A"
        product_url = "https://www.sirena.do" + title_element["href"] if title_element else ""

        # Extraer la imagen
        image_style = item.select_one(".item-product-image")["style"]
        image_url = image_style.split("url(")[-1].strip('");') if image_style else ""

        # Precio
        price_element = item.select_one(".item-product-price strong")
        price = price_element.text.strip() if price_element else "N/A"

        # Descuento (si existe)
        discount_element = item.select_one(".item-product-discount strong")
        discount = discount_element.text.strip() if discount_element else "0%"

        # Categoría
        category_element = item.select_one(".item-product-cat a")
        category = category_element.text.strip() if category_element else "N/A"

        # Disponibilidad
        available = "No disponible" not in item.text

        # Agregar al JSON
        productos.append({
            "id": product_id,
            "title": title,
            "url": product_url,
            "image_url": image_url,
            "price": price,
            "discount": discount,
            "category": category,
            "available": available
        })
    return productos

# Función para obtener el número total de páginas
def get_total_pages(soup):
    pagination = soup.find("ul", class_="uk-pagination")
    if pagination:
        last_page = pagination.find_all("li")[-2].text.strip()  # El penúltimo li es la última página
        return int(last_page)
    return 1

# Lista para almacenar todos los productos
all_productos = []

# Obtener la primera página para detectar el número total de páginas
driver.get(base_url.format(1))
time.sleep(5)  # Esperar a que cargue la página
soup = BeautifulSoup(driver.page_source, "html.parser")
total_pages = get_total_pages(soup)

# Iterar sobre cada página
for page in range(1, total_pages + 1):
    print(f"Scraping página {page} de {total_pages}...")
    driver.get(base_url.format(page))
    time.sleep(5)  # Esperar a que cargue la página
    soup = BeautifulSoup(driver.page_source, "html.parser")
    productos = extract_products(soup)
    all_productos.extend(productos)

# Cerrar Selenium
driver.quit()

# Guardar en JSON
with open("data/ropa.json", "w", encoding="utf-8") as f:
    json.dump(all_productos, f, indent=4, ensure_ascii=False)

print("✅ Scraping completado. Datos guardados en 'productos3.json'")