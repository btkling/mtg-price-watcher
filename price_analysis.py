import pandas as pd
from datetime import datetime as dt

def read_price_data(filepath=None):
    if filepath:
        df = pd.read_csv(filepath + "price_tracker.csv")
    else:
        df = pd.read_csv("price_tracker.csv")
    
    return df

# TODO analyze card trends


def print_desired(price_history, lookback_days):
    '''
    Given a data frame (price history), print out the entries that have a desired price in the past 48 hours.
    '''
    lookback = pd.to_datetime(dt.today()) - pd.Timedelta(lookback_days, unit='day')

    price_history_lookback = price_history[pd.to_datetime(price_history["checked_timestamp"]) >= lookback]
    price_history_lookback_valid = price_history_lookback[ price_history_lookback["is_desired"] == True ]
    
    print(price_history_lookback_valid.head(100))
    return


# TODO predict cards that will achieve desired price in next n days


# TODO cheapest current printing, full price history
def cheapest_history(price_history):
    '''
    Given a data frame (price_history), return a new dataframe subset to the
    elements of the original where only the price history of the cheapest printing of each 
    card is returned
    '''


def main():
    print("hello")
    fp = "/mnt/e/git/mtg-price-watcher/"
    price_history = read_price_data()
    print(price_history.head())
    print_desired(price_history, 2)

if __name__ == "__main__":
    main()