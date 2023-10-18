import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.buyrentkenya.com/'
url = 'https://www.buyrentkenya.com/flats-apartments-for-rent'

Location = []
City = []
Price = []
Area = []
Bedrooms = []
Bathrooms = []
Generator = []
Furnished = []
Internet = []
Gym = []
Balcony = []
Parking = []
Ensuite = []
Lift = []

for page in range(201, 217):
    if page == 1:
        page_url = url
    else:
        page_url = f'{url}?page={page}'
    page_response = requests.get(page_url)
    if page_response.status_code != 200:
        print(f"Page {page} request failed")
        continue
    page_soup = BeautifulSoup(page_response.text, 'lxml')
    house_urls = page_soup.find_all('h2', class_='md:hidden mb-3 font-semibold')
    for house in house_urls:
        house_url = base_url.rstrip('/') + house.a['href']
        house_response = requests.get(house_url)
        if house_response.status_code != 200:
            print('House request failed')
            continue
        house_soup = BeautifulSoup(house_response.text, 'lxml')

        try:
            city = house_soup.find('ul', class_='list-reset flex flex-nowrap text-xs font-extralight overflow-x-auto h-8 scrollbar-hidden font-normal').find_all('li', class_="flex items-center whitespace-nowrap")[3].text.strip()
        except AttributeError:
            city = None
        try:
            location = house_soup.find('ul', class_='list-reset flex flex-nowrap text-xs font-extralight overflow-x-auto h-8 scrollbar-hidden font-normal').find_all('li', class_="flex items-center whitespace-nowrap")[4].text.strip()
        except AttributeError:
            location = None
        except IndexError:
            location = None
        try:
            area = house_soup.find('div', class_='flex flex-wrap md:justify-start w-full md:w-auto my-4 overflow-hidden').find('span', class_='flex items-center mr-5 max-w-24').text.strip()
        except AttributeError:
            area = None
        try:
            bedrooms = house_soup.find('div', class_='flex flex-wrap md:justify-start w-full md:w-auto my-4 overflow-hidden').find('span', class_='flex items-center mr-5 max-w-24 truncate').text.strip()
        except AttributeError:
            bedrooms = None
        try:
            bathrooms = house_soup.find('div', class_='flex flex-wrap md:justify-start w-full md:w-auto my-4 overflow-hidden').find('span', class_='flex items-center max-w-24 truncate').text.strip()
        except AttributeError:
            bathrooms = None
        try:
            ammenities = house_soup.find('div', class_='grid md:grid-cols-2 gap-5 w-full').find_all('div', class_='flex flex-col pb-2')
            house_details = []
            for k in ammenities:
                features = k.find('ul', class_='items-center flex flex-row flex-wrap').find_all('li')
                for feat in features:
                    house_details.append(feat.find('div').text.split())
            house_details = [item for sublist in house_details for item in sublist]
        
            generator = 0
            furnished = 0
            gym = 0
            parking = 0
            lift = 0
            internet = 0
            balcony = 0
            ensuite = 0
            for i in house_details:
                if i.lower() == 'generator':
                    generator = 1
                elif i.lower() == 'furnished':
                    furnished = 1
                elif i.lower() == 'gym':
                    gym = 1
                elif i.lower() == 'parking':
                    parking = 1
                elif i.lower() == 'lift':
                    lift = 1
                elif i.lower() == 'internet':
                    internet = 1
                elif i.lower() == 'balcony':
                    balcony = 1
                elif i.lower() == 'suite':
                    ensuite = 1
        except AttributeError:
            generator = furnished = gym = parking = lift = internet = balcony = ensuite = None
        try:
            price = house_soup.find('div', class_='flex justify-end items-end space-x-2 ml-auto').find('span', class_='md:text-xxl font-extrabold block').text.split()
            price = price[1]
        except AttributeError:
            price = None
        Location.append(location)
        City.append(city)
        Price.append(price)
        Area.append(area)
        Bedrooms.append(bedrooms)
        Bathrooms.append(bathrooms)
        Generator.append(generator)
        Furnished.append(furnished)
        Internet.append(internet)
        Gym.append(gym)
        Balcony.append(balcony)
        Parking.append(parking)
        Ensuite.append(ensuite)
        Lift.append(lift)
    print(f'Page {page} Done')
    if page % 20 == 0 or page == 216:
        house_data = {"City": City, "Location": Location, "Area": Area, "Bedrooms": Bedrooms, "Bathrooms": Bathrooms, "Generator": Generator, "Furnished": Furnished,
                    "Internet": Internet, "Gym": Gym, "Balcony": Balcony, "Parking": Parking, "Ensuite": Ensuite, "Lift": Lift, "Price": Price}

        df = pd.DataFrame(house_data)
        df.to_csv(f'buy_rent_kenya{page}.csv', index=False)
        break