import pandas as pd
import requests
from bs4 import BeautifulSoup

Price = []
Location = []
City = []
Bedrooms = []
Bathrooms = []
Parking = []

for page in range(8001, 10096):
    if page == 1:
        url = 'https://www.property24.co.ke/property-to-rent-in-nairobi-c1890'
    else:
        url = f'https://www.property24.co.ke/property-to-rent-in-nairobi-c1890?Page={page}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Page {page} failed')
        continue
    soup = BeautifulSoup(response.text, 'lxml')

    houses = soup.find_all('div', class_='pull-left sc_listingTileContent')

    for house in houses:
        try:
            price = house.find('div', class_='sc_listingTilePrice primaryColor').find('span').text.strip()
        except:
            price = None
        try:
            locality = house.find('div', class_='sc_listingTileAddress primaryColor').text.strip().split(',')
            location = locality[-2]
            city = locality[-1]
        except:
            location = None
            city = None
        try:
            details = house.find('div', class_='sc_listingTileIcons').find_all('span')
        except:
            details = None
        try:
            bedrooms = details[0].text.strip()
        except:
            bedrooms = None
        try:
            bathrooms = details[1].text.strip()
        except:
            bathrooms = None
        try:
            parking = details[2].text.strip()
        except:
            parking = None
        City.append(city)
        Location.append(location)
        Price.append(price)
        Bedrooms.append(bedrooms)
        Bathrooms.append(bathrooms)
        Parking.append(parking)
    if page % 100 == 0:
    	print(f'Page {page} Done')
    if page % 1000 == 0:
        data = {'Location': Location, 'City': City, 'Bedrooms': Bedrooms, 'Bathrooms': Bathrooms, 'Parking': Parking, 'Price': Price}
        df = pd.DataFrame(data)
        df.to_csv(f'property24_{page}.csv', index=False)

data = {'Location': Location, 'City': City, 'Bedrooms': Bedrooms, 'Bathrooms': Bathrooms, 'Parking': Parking, 'Price': Price}
df = pd.DataFrame(data)
df.to_csv('property24_final.csv', index=False)
