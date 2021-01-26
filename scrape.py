from bs4 import BeautifulSoup
from requests import get
from discord_webhook import DiscordWebhook, DiscordEmbed
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
import os
import schedule
import time

sns.set()

# Variables
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

prices     = []
addresses  = []
urls       = []
url        = [
        "https://www.redfin.com/city/6343/CA/Folsom/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/22597/CA/Fair-Oaks/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/22489/CA/El-Dorado-Hills/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0",
        "https://www.redfin.com/city/24782/CA/Orangevale/filter/max-price=600k,min-beds=3,min-sqft=1.75k-sqft,hoa=0"
]

# Webhook Varibales
webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/803149173531738112/eyX9efVcRfARXeEfKuv61139dhw43lYhCoHBf8dxJ5gwQaefgUB1S-asECBiTpozhRxr')

# File to Open
filepath = 'previous_houses.txt'

# Loop Through All URLs and get the Prices and Links for all houses
for u in url:
  response = get(u, headers=headers)
  html_soup = BeautifulSoup(response.text, 'html.parser')
  house_containers = html_soup.find_all('div', class_="v2 interactive")

  if house_containers != []:
    for container in house_containers:

       # Address of House
       address = container.find_all('div', class_="link-and-anchor")[0].text

       # Price of House
       price = container.find_all('span')[0].text
       link = 'https://www.redfin.com/' + container.find_all('a')[0].get('href')[1:]

       # Filter Out Houses that are at the bottom of the Scrapping Website
       if("Citrus Heights" in address):
         print(address)
         print(price)
         print(link)
       else:
         print('append to list')
         addresses.append(address)
         prices.append(price)
         urls.append(link)

# Filter out Duplicates stored in each array
addresses = list(dict.fromkeys(addresses))
prices = list(dict.fromkeys(prices))
urls = list(dict.fromkeys(urls))
print(urls)

#schedule.every(1).minutes.do(read_file)

#while True:
#    schedule.run_pending()
#    time.sleep(1)

# Open a file which will contain all the previous house listings
# Loop through the urls array and compare them with the file
# Then check for any URL duplicates so it won't be sent via the Discord Webhook twice
def read_file():
 with open(filepath, "r+") as fp:
  #for i in range(len(urls)):
     if(os.stat(filepath).st_size == 0):
       print('is empty')
       for i in range(len(urls)):
         fp.write(urls[i]+'\n')
     else:
       print('not empty')
       line = fp.readline()
       cnt = 1
       while line:
         for i in range(len(urls)):
           if(urls[i] == line.strip()):
             print('match: '+urls[i]+'\n')
             i+=1
           else:
             print('no match: '+urls[i])
             print('adding to discord...')
             #upload_to_discord(prices[i], addresses[i], urls[i])
             print('writing new url to file')
             fp.write(urls[i]+'\n')
           line = fp.readline()
           cnt += 1
  #fp.close()

def upload_to_discord(title, desc, url):
  # Since this URL was not found previously send message to Discord
  # Prepare Discord Message
  # create embed object for webhook
  embed = DiscordEmbed(title=title, description=desc+'\n'+url, color=242424)
  # set timestamp (default is now)
  embed.set_timestamp()
  # add embed object to webhook
  webhook.add_embed(embed)
  webhook_resp = webhook.execute()

read_file()
