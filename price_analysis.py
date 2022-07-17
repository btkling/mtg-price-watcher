from audioop import add
import pandas as pd
import numpy as np
from datetime import datetime as dt

def read_price_data(filepath=None):
    '''Read in data with price history
    
    # Parameters

    filepath: string, default=None
        optionally supply a filepath to the price data

    # Returns

    DataFrame with the price data
    '''
    if filepath is not None:
        df = pd.read_csv(filepath + "price_tracker.csv")
    else:
        df = pd.read_csv("price_tracker.csv")
    
    return df

def print_desired(price_history, lookback_days=2):
    '''
    Return the entries that have a desired price in the past ```lookback-days``` hours.

    # Parameters:
    
    price_history : DataFrame
        DataFrame with price information, output from watcher.py
    lookback_days: int, default 2
        number of days to scan back in time


    # Returns 

    None
    '''
    lookback = pd.to_datetime(dt.today()) - pd.Timedelta(lookback_days, unit='day')

    price_history_lookback = price_history[pd.to_datetime(price_history["checked_timestamp"]) >= lookback]
    price_history_lookback_valid = price_history_lookback[ price_history_lookback["is_desired"] == True ]
    
    print(price_history_lookback_valid.head(100))
    # TODO refactor this to return a DataFrame
    return


def desire_predictor(price_history, future_days=7):
    '''
    Find all card/set/cn combinations that we predict to achieve desired price in the next n days

    # Parameters:
    :price_history: DataFrame, the dataframe containing the price information, output from watcher.py

    :future_days: int(default 7), number of days to look forward

    # Return:
    DataFrame - frame with all Card / Set / Collector Number combinations meeting the prediction criteria
    
    '''
    return price_history
    # TODO predict cards that will achieve desired price in next n days


def cheapest_history(price_history : pd.DataFrame, num_entries=-1):
    '''
    Returns the price history of the cheapest printing of each card

    # Parameters:

    price_history : DataFrame
        the dataframe containing the price information, output from watcher.py
    num_entries : integer, default -1
        number of historical price records to return
    '''

    maxdate = price_history.groupby(["card_name", "set_code", "collector_num"]).agg({"checked_timestamp" : "max"}).reset_index()

    latest_record = maxdate.merge(price_history, 
                            left_on=["card_name", "set_code", "collector_num", "checked_timestamp"],
                            right_on=["card_name", "set_code", "collector_num", "checked_timestamp"])

    
    latest_record = latest_record[~np.isnan(latest_record["price_usd"])]

    lowest_price = latest_record.groupby("card_name").agg({"price_usd" : "min"})

    cards_to_join = latest_record.merge(lowest_price,   
                                        left_on = ["card_name", "price_usd"],
                                        right_on = ["card_name", "price_usd"])

    full_set_lowest = price_history.merge(cards_to_join,
                                          left_on=["card_name", "set_code", "collector_num"],
                                          right_on=["card_name", "set_code", "collector_num"],
                                          suffixes=("", "_ctj"))
    
    if num_entries > -1:
        full_set_lowest = full_set_lowest.groupby(["card_name", "set_code", "collector_num"]).tail(num_entries).reset_index(drop=True)
    
    return full_set_lowest[["checked_timestamp",
                            "card_name",
                            "set_code",
                            "set_name",
                            "collector_num",
                            "price_usd",
                            "desired_price",
                            "diff_to_desired",
                            "is_desired",
                            "tcgplayer_uri"]]

def add_moving_avg(price_history: pd.DataFrame, usecheapest=True, remove_nan=False, return_last=True):
    '''Plot a moving average for each unique card combination
    
    # Parameters:
    
    price_history : DataFrame
        the DataFrame containing all of the price information that we want to examine
    destfile : str, default None
        if you want to specify a destination filename for the printings to go
    usecheapest : bool, default True
        print only the records from the cheapest printing of the card
    remove_nan : bool, default False
        remove entries without a SMA entry?
    return_last : bool, default True
        remove all but the last entry for each card?

    # Returns:

    A DataFrame with the simple moving average (7 day) for the cards
    '''

    if usecheapest:
        price_history = cheapest_history(price_history)

    price_history = price_history.sort_values(["card_name","set_code", "collector_num","checked_timestamp"], ascending=True).reset_index(drop=True)

    price_history["price_usd_SMA7"] = price_history.groupby(["card_name", "set_code", "collector_num"]).rolling(7)["price_usd"].mean().reset_index(drop=True)

    price_history["price_usd_SMA_delta"] = price_history["price_usd"] - price_history["price_usd_SMA7"]

    if remove_nan:
        price_history = price_history[~np.isnan(price_history["price_usd_SMA7"])].reset_index()
    
    if return_last:
        price_history = price_history.groupby(["card_name","set_code","set_name","collector_num"]).tail(1).reset_index(drop=True)

    return price_history


def main():
    fp = "/mnt/e/git/mtg-price-watcher/"
    price_history = read_price_data()
    # print(price_history.head())
    print_desired(price_history, 2)
    print(cheapest_history(price_history, 1)[["card_name", "set_code", "collector_num", "price_usd", "desired_price"]])

    price_history = add_moving_avg(price_history)

if __name__ == "__main__":
    main()