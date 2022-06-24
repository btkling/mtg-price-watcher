from cmath import isnan
from time import sleep
import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt


def build_card_df(card_name, desired_price):
    scryfall_api_url = "https://api.scryfall.com/cards/search?q="+card_name+"&unique=prints"
    api_response = requests.get(scryfall_api_url).json()
    i = 0

    cards_data = pd.DataFrame()
    # Get all of the IDs

    for count, val in enumerate(api_response['data']):
        #id_all.append(val['tcgplayer_id'])
        card_name = val['name']
        set_code = val['set']
        set_name = val['set_name']
        price = val['prices']['usd']
        card = pd.DataFrame(
                {
                    "card_name": card_name,
                    "set_code": set_code,
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
    cards_data = cards_data[np.isnan(cards_data["price_usd"]) == False] 

    # add a field to compare price to desired price
    cards_data['diff_to_desired'] = cards_data["price_usd"] - desired_price
    cards_data['desired_price'] = cards_data["price_usd"] <= desired_price

    return cards_data.sort_values(by=["price_usd"])

def read_cards_to_check():
    df = pd.read_csv("cards_to_check.csv", header=0)
    return df




def main():
    MILLISECONDS_DELAY = 100 # Scryfall requests a 50-100 Millisecond delay between requests

    cards_to_check = read_cards_to_check()
    print(cards_to_check.head())
    # print(cards_to_check.columns())

    for card in cards_to_check.itertuples():
        card_name = card[1]
        desired_price = card[2]
        print(f"Card Name: {card_name} || Desired Price: {desired_price}")
        price_data = build_card_df(card_name, desired_price)
        print(price_data.head())
        sleep(MILLISECONDS_DELAY/1000)

    # price_data = build_card_df(cards_to_check['card_name'][0], cards_to_check['desired_price'][0])
    # print(price_data.head())

if __name__ == "__main__":
    main()