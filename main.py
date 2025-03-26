import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_vehicle_data(url):
    response = requests.get(url)
    if response.ok:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        return None

def extract_vehicle_info(soup):
    vehicle_data = {}
    container = soup.find('div', id='detail-left')
    header = container.find('div', id='detail-ad-header')
    vehicle_data['name_prod'] = header.find('h1').text.strip()
    vehicle_data['cost_prod'] = header.find('h3').text.strip()
    vehicle_data['info_publicacion'] = header.find('div').text.strip()

    car_info_specs = container.find('div', id='detail-ad-info-specs')
    vehicle_data['transmision'] = car_info_specs.find_all('strong')[0].text.strip()
    vehicle_data['Traccion'] = car_info_specs.find_all('strong')[1].text.strip()
    vehicle_data['combustible'] = car_info_specs.find_all('strong')[2].text.strip()
    vehicle_data['color'] = car_info_specs.find_all('strong')[3].text.strip()

    car_specs_table = container.find('table')
    rows = car_specs_table.find_all('tr')
    vehicle_data['precio'] = rows[0].text.strip()
    vehicle_data['motor'] = rows[1].text.strip()
    vehicle_data['Exterior_Tipo'] = rows[2].text.strip()
    vehicle_data['Interior_Uso'] = rows[3].text.strip()
    vehicle_data['Combustible_Carga'] = rows[4].text.strip()
    vehicle_data['Transmision_Puertas'] = rows[5].text.strip()
    vehicle_data['Traccion_pasajero'] = rows[6].text.strip()

    if len(container.find_all('div', class_='detail-ad-info-specs-block')) == 6:
        accesorios = [accesorio.text.strip() for accesorio in container.find_all('div', class_='detail-ad-info-specs-block')[-3].find_all('li')[:-2]]
        observaciones = container.find_all('div', class_='detail-ad-info-specs-block')[-2].text.strip()
    else:
        accesorios = [accesorio.text.strip() for accesorio in container.find_all('div', class_='detail-ad-info-specs-block')[-2].find_all('li')[:-2]]
        observaciones = None

    vehicle_data['accesorios'] = accesorios
    vehicle_data['observaciones'] = observaciones

    return vehicle_data

def get_seller_info(soup):
    seller_info = {}
    container_right = soup.find('div', id='detail-right')
    seller_info['img_logo_vendedor'] = container_right.find('div', class_='logo').find('img').get('src').strip()
    seller_info['nam_vendedor'] = container_right.find('h3').text.strip()
    seller_info['tipo_vendedor'] = container_right.find('div', class_='sub-text').text.strip()
    seller_info['info_vendedor'] = [accesorio.text.strip() for accesorio in container_right.find_all('li')]
    
    url_map = container_right.find('iframe', class_='map').get('src')
    if url_map:
        coordenadas = url_map.split('/')[-1].split('&')[0].split('=')[-1].split(',')
    else:
        coordenadas = None
    
    seller_info['Coordenadas'] = coordenadas
    
    return seller_info

def save_to_excel(data, filename='supercarro.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    url_mazda = 'https://www.supercarros.com/mazda-cx5/1401704/'
    url_kia = 'https://www.supercarros.com/kia-picanto/1368500/'

    mazda_soup = get_vehicle_data(url_mazda)
    # kia_soup = get_vehicle_data(url_kia)

    if mazda_soup:
        mazda_data = extract_vehicle_info(mazda_soup)
        mazda_seller_info = get_seller_info(mazda_soup)
        mazda_data.update(mazda_seller_info)
        save_to_excel([mazda_data])

    # if kia_soup:
    #     kia_data = extract_vehicle_info(kia_soup)
    #     kia_seller_info = get_seller_info(kia_soup)
    #     kia_data.update(kia_seller_info)
    #     save_to_excel([kia_data])

if __name__ == "__main__":
    main()

# for index, row  in autos_.iterrows():
#     print(index, row)
   
# # response = requests.get(row['Link'])
# url_m =    'https://www.supercarros.com/mazda-cx5/1401704/'
# url_kia = 'https://www.supercarros.com/kia-picanto/1368500/'
# response = requests.get(url_kia)


# if response.ok:
   
#     vehicles_data1 = []
   
#     html = response.content
#     soup = BeautifulSoup(html,'html.parser')
   
   
#     # Seleccionar el div que contiene la informacion del auto
    
#     container = soup.find('div',
#     id='detail-left')
    
    
#     #header
    
#     header = container.find('div',id='detail-ad-header')
    
    
#     name_prod = header.find('h1').text.strip()
    
#     cost_prod = header.find('h3').text.strip()
    
#     info_publicacion = header.find('div').text.strip()
    
    
    
#     # # Asegurarse de buscar dentro del div específico
    
#     car_info_specs = container.find('div',id='detail-ad-info-specs')
    
    
#     trnasmision = car_info_specs.find_all('strong')[0].text.strip()
    
#     Traccion = car_info_specs.find_all('strong')[1].text.strip()
    
#     combustible = car_info_specs.find_all('strong')[2].text.strip()
    
#     color = car_info_specs.find_all('strong')[3].text.strip()
    

#     car_specs_table = container.find('table')
    
    
#     precio = car_specs_table.find_all('tr')[0].text.strip()
    
#     motor = car_specs_table.find_all('tr')[1].text.strip()
    
#     exterior_tipo = car_specs_table.find_all('tr')[2].text.strip()
    
#     interior_uso = car_specs_table.find_all('tr')[3].text.strip()
    
#     combustible_carga = car_specs_table.find_all('tr')[4].text.strip()
    
#     transmision_puertas = car_specs_table.find_all('tr')[5].text.strip()
    
#     traccion_pasajero = car_specs_table.find_all('tr')[6].text.strip()
    


   
#     if len(container.find_all('div',class_='detail-ad-info-specs-block')) == 6:
           
#         accesorios = [accesorio.text.strip()
#         for accesorio in  container.find_all('div',class_='detail-ad-info-specs-block')[-3].find_all('li')[:-2]]

#         observaciones = container.find_all('div',class_='detail-ad-info-specs-block')[-2].text.strip()#.find_all('li')[:-2]


#     else:
           
#         accesorios = [accesorio.text.strip()
                      
#     for accesorio in container.find_all('div',class_= 'detail-ad-info-specs-block' )[-2].find_all('li')[:-2]]
               
#         observaciones =  None
    
    
    
    
    
    
#     container_right = soup.find('div',id='detail-right')
    
    
#     img_logo_vendedor = container_right.find('div',class_='logo').find('img').get('src').strip()
    
#     nam_vendedor = container_right.find('h3').text.strip()
    
#     tipo_vendedor = container_right.find('div',class_='sub-text').text.strip()
    
#     info_vendedor = [accesorio.text.strip()
#     for accesorio in container_right.find_all('li')]
    
    
#     url_map = container_right.find('iframe',class_='map').get('src')
    
#     if url_map:
           
#     # https://www.google.com/maps/embed/v1/
           
#     # place?q=19.4661775,-70.6864214¢er=
           
#     # 19.4661775,-70.6864214
           
#     # &zoom=15&key=AIzaS\\..pho.
           
#         coordenadas =  url_map.split('/')[-1].split('&')[0].split('=')[-1].split(',')
           
           
    
#     else:
           
#         coordenadas = None
           
           
    
#     vehicles_data1.append({'name_prod' : name_prod,
#                             'cost_prod' : cost_prod,
#                             'info_publicacion' : info_publicacion,
#                             'transmision': trnasmision,
#                             'Traccion' : Traccion,
#                             'combustible' : combustible,
#                             'color' : color,
#                             'precio' : precio,
#                             'motor' : motor,
#                             'Exterior_Tipo' : exterior_tipo,
#                             'Interior_Uso' : interior_uso,
#                             'Combustible_Carga' : combustible_carga,
#                             'Transmision_Puertas' : transmision_puertas,
#                             'Traccion_pasajero':traccion_pasajero,
#                             'accesorios' : accesorios,
#                             'observaciones' : observaciones,
#                             'logo_vendedor' : img_logo_vendedor,                                         
#                             'nam_vendedor' : nam_vendedor,
#                             'tipo_vendedor' : tipo_vendedor,
#                             'info_vendedor' : info_vendedor,
#                             'Coordenadas' : coordenadas
#                                           }
#                                           )#'Link':Link
    
#     df_cars = pd.DataFrame(vehicles_data1)
    
#     df_cars.to_excel('supercarro.xlsx',index=False)
