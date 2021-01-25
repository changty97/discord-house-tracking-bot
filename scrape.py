from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
from discord_webhook import DiscordWebhook, DiscordEmbed
#from discordwebhook import Discord

sns.set()

# Variables
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

prices     = []
#thumbnails = []
titles     = []
urls       = []
url        = [
        "https://www.redfin.com/city/6343/CA/Folsom/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/22597/CA/Fair-Oaks/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/22489/CA/El-Dorado-Hills/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/24782/CA/Orangevale/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0"
]

# Webhook Varibales
webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/803149173531738112/eyX9efVcRfARXeEfKuv61139dhw43lYhCoHBf8dxJ5gwQaefgUB1S-asECBiTpozhRxr')

# Loop Through All URLs and get the Prices and Links for all houses
for u in url:
  response = get(u, headers=headers)
  html_soup = BeautifulSoup(response.text, 'html.parser')
  house_containers = html_soup.find_all('div', class_="v2 interactive")

  if house_containers != []:
    for container in house_containers:
       # Thumbnails
       #img = str(container.find_all('img'))
       #img = img[img.find('data-original_2x=')+18:img.find('id=')-2]
       #thumbnails.append(img)

       # Title
       title = container.find_all('div', class_="link-and-anchor")[0].text
       titles.append(title)

       # Price
       price = container.find_all('span')[0].text
       prices.append(price)

       # url
       link = 'https://www.redfin.com/' + container.find_all('a')[0].get('href')[1:]
       urls.append(link)
       print('\n')

titles = list(dict.fromkeys(titles))
print(titles)

prices = list(dict.fromkeys(prices))
print(prices)

urls = list(dict.fromkeys(urls))
print(urls)

# Prepare Discord Message
# create embed object for webhook
embed = DiscordEmbed(title=prices[0], description=titles[0]+'\n'+urls[0], color=242424)

# set thumbnail
embed.set_thumbnail(url=urls[0])

# set timestamp (default is now)
embed.set_timestamp()

# add embed object to webhook
webhook.add_embed(embed)
webhook_resp = webhook.execute()
