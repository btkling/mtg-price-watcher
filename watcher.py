from cmath import isnan
from time import sleep
import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt
from os.path import exists

def build_card_df(card_name, desired_price, remove_blanks=True, only_desired=False):
    scryfall_api_url = "https://api.scryfall.com/cards/search?q="+card_name+"&unique=prints"
    api_response = requests.get(scryfall_api_url).json()
    i = 0

    cards_data = pd.DataFrame()
    # Get all of the IDs

    for count, val in enumerate(api_response['data']):
        # digital only cards will not have a link to TCG Player
        if(val['digital']):
            continue

        card_name = val['name']
        set_code = val['set']
        set_name = val['set_name']
        collector_num = val['collector_number']
        price = val['prices']['usd']
        if(np.float64(price)<=desired_price):
            tcgplayer_uri = val['purchase_uris']['tcgplayer']
        else:
            tcgplayer_uri = ""
        card = pd.DataFrame(
                {
                    "card_name": card_name,
                    "set_code": set_code,
                    "set_name": set_name,
                    "collector_num": collector_num,
                    "price_usd": price,
                    "tcgplayer_uri": tcgplayer_uri,
                    "checked_timestamp": pd.to_datetime(dt.today())
                },
                index = [i]
            )
        cards_data = pd.concat([cards_data, card])
        i += 1

    # some prices are missing, and price needs to be a floating point value
    cards_data['price_usd'] = np.float64(cards_data["price_usd"])
    if(remove_blanks):
        cards_data = cards_data[np.isnan(cards_data["price_usd"]) == False] 

    # add a field to compare price to desired price
    cards_data['diff_to_desired'] = round(cards_data["price_usd"] - desired_price, 2)
    cards_data['desired_price'] = desired_price
    cards_data['is_desired'] = cards_data["price_usd"] <= desired_price

    if(only_desired):
        cards_data = cards_data[cards_data["price_usd"]<= desired_price]

    output = cards_data.reset_index()[["checked_timestamp",
                        "card_name",
                        "set_code",
                        "set_name",
                        "collector_num",
                        "price_usd",
                        "desired_price",
                        "diff_to_desired",
                        "is_desired",
                        "tcgplayer_uri"
                        ]]

    return output.sort_values(by=["price_usd"])

def read_cards_to_check(fp=None):
    if fp:
        df = pd.read_csv(fp + "cards_to_check.csv", header=0)
    else:
        df = pd.read_csv("cards_to_check.csv", header=0)
    return df




def main():
    MILLISECONDS_DELAY = 100 # Scryfall requests a 50-100 Millisecond delay between requests

    fp = "/mnt/e/git/mtg-price-watcher/"

    cards_to_check = read_cards_to_check(fp)

    for card in cards_to_check.itertuples():
        card_name = card[1]
        desired_price = card[2]
        print("")
        print("--------------------------------------------------------------")
        print(f"Card Name: {card_name} || Desired Price: {desired_price}")
        print("--------------------------------------------------------------")
        price_data = build_card_df(card_name, desired_price, remove_blanks=False)
        print(price_data.head())
        sleep(MILLISECONDS_DELAY/1000)

        if fp:
            if(not exists(fp+"price_tracker.csv")):
                price_data.to_csv(fp+'price_tracker.csv',mode='w', index=False)    
            else:
                price_data.to_csv(fp+'price_tracker.csv',mode='a', header=False, index=False)
        else:
            if(not exists("price_tracker.csv")):
                price_data.to_csv('price_tracker.csv',mode='w', index=False)    
            else:
                price_data.to_csv('price_tracker.csv',mode='a', header=False, index=False)

if __name__ == "__main__":
    main()