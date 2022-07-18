import pandas as pd
import price_analysis as pran
import smtplib 
import ssl
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


    port = 465 # for SSL
    email = jscfg["email"]
    password = jscfg["password"]

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        print("yay")
        server.sendmail(email, email, f"Subject: HELLO!\nBody of email.\n I am a test.")

if __name__ == "__main__":
    main()