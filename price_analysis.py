import pandas as pd
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


# TODO cheapest current printing, full price history
def cheapest_history(price_history, num_entries=-1):
    '''
    #TODO finish Doc String
    Returns the price history of the cheapest printing of each card

    # Parameters:

    price_history : DataFrame
        the dataframe containing the price information, output from watcher.py
    num_entries : integer, default -1
        number of historical price records to return
    '''

    '''
    PSEUDO -- STEPS
    ===========================================================
    1. GET MOST RECENT PRICE FOR EACH CARD/SET/COLLECTOR NUMBER
    2. GET LOWEST PRICE FOR EACH CARD -> RECORD SET/CN
    3. JOIN BACK TO ORIG DATA WITH CARD/SET/CN MATCH
    4. RETURN PRICE HISTORY, LIMITED TO MOST RECENT N ENTRIES
        DEFAULTS TO RETURN ALL ENTRIES
    ===========================================================
    '''
    return price_history


def main():
    fp = "/mnt/e/git/mtg-price-watcher/"
    price_history = read_price_data()
    print(price_history.head())
    print_desired(price_history, 2)

if __name__ == "__main__":
    main()