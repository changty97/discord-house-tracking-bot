from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
#prices = []
urls   = []
url    = [
        "https://www.redfin.com/city/6343/CA/Folsom/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/22597/CA/Fair-Oaks/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/22489/CA/El-Dorado-Hills/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/24782/CA/Orangevale/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0"
]

for u in url:
  response = get(u, headers=headers)
  print(response)

  html_soup = BeautifulSoup(response.text, 'html.parser')
  house_containers = html_soup.find_all('div', class_="v2 interactive")

  if house_containers != []:
    for container in house_containers:
      # Price
      #price = container.find_all('span')[2].text
      #if price == 'Contacte Anunciante':
       # price = container.find_all('span')[3].text
       # if price.find('/') != -1:
       #   price = price[0:price.find('/')-1]
       #   if price.find('/') != -1:
       #     price = price[0:price.find('/')-1]

       #price_ = [int(price[s]) for s in range(0,len(price)) if price[s].isdigit()]
       #price = ''
       #for x in price_:
       #  price = price+str(x)
       #prices.append(int(price))

      # url
      link = 'https://www.redfin.com/' + container.find_all('a')[0].get('href')[1:]
      urls.append(link)
      print('\n')

urls = list(dict.fromkeys(urls))
print(urls)
