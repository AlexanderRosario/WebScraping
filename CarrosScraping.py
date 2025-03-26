import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

base_url = "https://www.supercarros.com"
vehicles_data = []

# Obtener el HTML de la página principal
response = requests.get(base_url)
if response.ok:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrar la sección que contiene los enlaces de interés
    types_section = soup.find('div', class_='homerow-1-left-types')

    # Encontrar todos los enlaces dentro de la sección
    type_links = types_section.find_all('a', href=True)

    for link in type_links:
        type_url = base_url + link['href'] # Obtener la URL completa
        print(f"Scraping de: {type_url}")

        # Realizar web scraping y paginación para cada enlace
        current_page = 0
        while True:
            # Construir la URL de la página actual
            url = f'{type_url}/?PagingPageSkip={current_page}'
            response = requests.get(url)

            if response.ok:
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')

                # Seleccionar el div que contiene los listados de vehículos
                container = soup.find('div', id='bigsearch-results-inner-results')

                # Asegurarse de buscar dentro del div específico
                cars = container.find_all('li', class_='normal')

                for car in cars:
                    data_id = car['data-id']
                    data_photos = car['data-photos']
                    price = car.find('div', class_='price').text.strip()
                    year = car.find('div', class_='year').text.strip()
                    photoreal = car.find('img', class_='real')['src']
                    title1 = car.find('div', class_='title1').text.strip()
                    title2 = car.find('div', class_='title2').text.strip()
                    link = base_url + car.find('a')['href']

                    # Añadir el diccionario con los datos del vehículo a la lista
                    vehicles_data.append({'ID': data_id,
                                          'Photos_data': data_photos,
                                          'Photo': photoreal,
                                          'Price': price,
                                          'Year': year,
                                          'Title': title1,
                                          'Description': title2,
                                          'Link': link})

                    print(f"Photos: {photoreal}")

                # Intentar encontrar el enlace de la página siguiente
                pagination_container = soup.find('div', id='bigsearch-results-inner-lowerbar-pages')

                if pagination_container:
                    links = pagination_container.find_all('a')
                    next_page_link = links[-1]['href']
                    next_page_skip = next_page_link.split('=')[-1]

                    if int(next_page_skip) > current_page:
                        current_page = int(next_page_skip)
                    else:
                        break
                else:
                    break # No se encontró el contenedor de paginación, salir del bucle

                time.sleep(1) # Esperar un segundo antes de la próxima solicitud para no sobrecargar el servidor

            else:
                print("Error al obtener la página")
                break

# Convertir los datos recopilados en un DataFrame y guardarlos en un archivo Excel
vehicles_df = pd.DataFrame(vehicles_data)
vehicles_df.to_excel('vehicles_data.xlsx', index=False)
print('PROCESO TERMINADO...')