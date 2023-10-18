import pandas as pd
import requests
from bs4 import BeautifulSoup

City = []
Location = []
Price = []
Bedrooms = []
Bathrooms = []
Toilets = []

for page in range(451, 500):
    if page == 1:
        url = 'https://www.propertypro.co.ke/in/nairobi/'
    else:
        url = f'https://www.propertypro.co.ke/in/nairobi/?page={page}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Page {page} request failed')
        continue
    soup = BeautifulSoup(response.text, 'lxml')
    houses = soup.find_all('div', class_='single-room-text')
    for house in houses:
        try:
            locality = house.find('h4').text.strip()
            locality = locality.split()
            location = locality[0]
            city = locality[1]
        except:
            location = None
            city = None
        try:
            pricing = house.find('h3', class_='listings-price').find_all('span')
            price = pricing[1].text.strip()
        except:
            price = None
        try:
            interior = house.find_all('div', class_='fur-areea')
            interior = interior[0].text.strip().split('\n')
            bedrooms = interior[0]
            bathrooms = interior[1]
            toilets = interior[2]

        except:
            bedrooms = None
            bathrooms = None
            toilets = None
            
        City.append(city)
        Price.append(price)
        Location.append(location)
        Bedrooms.append(bedrooms)
        Bathrooms.append(bathrooms)
        Toilets.append(toilets)
    print(f"Page {page} Done")

data = {"City": City, "Location": Location, "Bedrooms": Bedrooms, "Bathrooms": Bathrooms, "Toilets": Toilets, "Price": Price}

df = pd.DataFrame(data)

df.to_csv(f'property_pro{page}.csv', index=False)