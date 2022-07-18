import pandas as pd
import price_analysis as pran
import smtplib 
import json

def load_config(file_path):
    '''Load the config file for email account
    
    # Parameters
    
    file_path : str
        the path to the file
    
    # Returns
    
    a dictionary with the parsed json'''

    file_handler = open(file_path)
    jscfg = json.load(file_handler)

    return jscfg

def main():
    print("hi")

    jscfg = load_config("config.json")
    print(jscfg)
    for k,v in jscfg.items():
        print(f"Key {k} || Value {v}")

if __name__ == "__main__":
    main()