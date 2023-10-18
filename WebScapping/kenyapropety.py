import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

start_time = time.time()

Price = []
City = []
Location = []
Bedrooms = []
Bathrooms = []
Parking = []
Toilets = []

for page in range(1, 100):
    if page == 1:
        url = 'https://kenyapropertycentre.com/for-rent'
    else:
        url = f'https://kenyapropertycentre.com/for-rent?page={page}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Page {page} request failed")
        continue
    soup = BeautifulSoup(response.text, 'lxml')
    houses = soup.find_all('div', class_='row property-list')
    for house in houses:
        pricing = house.find('span', class_='pull-sm-left').find_all('span')
        try:
            price = pricing[1].text.strip()
        except:
            price = None
        loc = house.find('address', class_='voffset-bottom-10').text.strip().split(',')
        try:
            city = loc[2]
            location = loc[1]
        except:
            city = None
            location = None
        interior = house.find('div', class_='wp-block-footer').find('ul', class_='aux-info').find_all('li')
        try:
            bedrooms = interior[0].find('span').text.strip()
        except:
            bedrooms = None
        try:
            bathrooms = interior[1].find('span').text.strip()
        except:
            bathrooms = None
        try:
            toilets = interior[2].find('span').text.strip()
        except:
            toilets = None
        try:
            parking = interior[3].find('span').text.strip()
        except:
            parking = None

        City.append(city)
        Location.append(location)
        Price.append(price)
        Bedrooms.append(bedrooms)
        Bathrooms.append(bathrooms)
        Toilets.append(toilets)
        Parking.append(parking)
    print(f'Page {page} Done')

data = {'City': City, 'Location': Location, 'Bedrooms': Bedrooms, 'Bathrooms': Bathrooms, 'Toilets': Toilets, 'Parking': Parking,'Price': Price}
df = pd.DataFrame(data)
df.to_csv('kenya_property.csv', index=False)

end_time = time.time()
exec_time = end_time - start_time
print(f'Took {exec_time} to scrape the website')