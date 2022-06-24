import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt


def build_card_df(card_name, desired_price):
    scryfall_api_url = "https://api.scryfall.com/cards/search?q="+card_name+"&unique=prints"
    api_response = requests.get(scryfall_api_url).json()
    i = 0

    cards_data = pd.DataFrame(columns = ["card_name", "set_name", "price_usd", "checked_timestamp"])
    # Get all of the IDs

    for count, val in enumerate(api_response['data']):
        #id_all.append(val['tcgplayer_id'])
        card_name = val['name']
        set_name = val['set_name']
        price = val['prices']['usd']
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
    
    # get minimum price
    minprice = cards_data.groupby("card_name").agg({'price_usd': 'min'}).reset_index()

    # trim dataset to only look at values where price = minprice
    cards_minprice = cards_data.merge(minprice, how="inner")


    return cards_data

    # check if price is less or equal to the desired price
    cards_data = cards_data[cards_data["price_usd"] <= desired_price]

    # return dataframe sorted by difference between actual and desired price







def main():
    # TODO refactor this to read an input file
    print("123")
    cards_to_check = ["Life from the Loam"]
    prices_to_check = [500]
    price_data = build_card_df(cards_to_check[0], prices_to_check[0])
    print(price_data.head(500))
    print("abc")

if __name__ == "__main__":
    main()