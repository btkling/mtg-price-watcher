import pandas as pd
from datetime import datetime as dt

def read_price_data(filepath=None):
    if filepath:
        df = pd.read_csv(filepath + "price_tracker.csv")
    else:
        df = pd.read_csv("price_tracker.csv")

    return df

# TODO analyze card trends

# TODO print records with a desired price

# TODO predict cards that will achieve desired price in next n days


def main():
    print("hello")
    fp = "/mnt/e/git/mtg-price-watcher/"
    price_history = read_price_data()
    print(price_history.head())

if __name__ == "__main__":
    main()