import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt

cards_to_check = ["bitterblossom"]
prices_to_check = [41]

scryfall_api_url = "https://api.scryfall.com/cards/search?q="+cards_to_check[0]+"&unique=prints"
api_response = requests.get(scryfall_api_url).json()

cards_data = pd.DataFrame(columns = ["card_name", "set_name", "price_usd", "checked_timestamp"])

i = 0
# Get all of the IDs
for count, val in enumerate(api_response['data']):
    #id_all.append(val['tcgplayer_id'])
    card_name = val['name']
    set_name = val['set_name']
    price = val['prices']['usd']
    #print(f"Card Name: {card_name} || Set Name: {set_name} || Price (USD): {price}")
    card = pd.DataFrame(
            {
                "card_name": card_name,
                "set_name": set_name,
                "price_usd": price,
                "checked_timestamp": pd.to_datetime(dt.now())
            },
            index = [i]
        )
    cards_data = pd.concat([cards_data, card])
    i += 1

# some prices are missing, and price needs to be a floating point value
cards_data['price_usd'] = np.float64(cards_data["price_usd"])

print(cards_data.head())
print(cards_data.info())

# get minimum price
minprice = cards_data.groupby("card_name").agg({'price_usd': 'min'}).reset_index()

# trim dataset to only look at values where price = minprice
cards_minprice = cards_data.merge(minprice, how="inner")

print(cards_minprice.head())



# check if price is less or equal to the desired price


# return dataframe sorted by difference between actual and desired price

