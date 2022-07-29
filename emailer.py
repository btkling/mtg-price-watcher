import pandas as pd
import numpy as np
import price_analysis as pran
import smtplib 
import ssl
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

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

def attach_file(attachment_file, mail : MIMEMultipart):
    '''attach a file to the mail object

    # Parameters

    attachment_file : str
        the file to be attached, assume that is in the same working directory
    mail : MIMEMultipart
        the mail object that we are building

    # Returns
    MIMEMultipart object with the file attached

    None
    '''
    file_path = attachment_file
    mimeBase = MIMEBase("application", "octet-stream")
    with open(file_path, "rb") as file:
        mimeBase.set_payload(file.read())
    encoders.encode_base64(mimeBase)
    mimeBase.add_header("Content-Disposition", f"attachment; filename={Path(file_path).name}")
    mail.attach(mimeBase)

    return mail



def main():

    ts = pd.Timestamp.now()
    date = ts.strftime("%A, %B %d %Y")
    time = ts.strftime("%I:%M %p")
    print(ts)
    print(f"Hello: today is {date}. The time now is {time}.")

    jscfg = load_config("config.json")
    # print(jscfg)
    # for k,v in jscfg.items():
        # print(f"Key {k} || Value {v}")


    PORT = 465 # for SSL
    from_email = jscfg["from_email"]
    to_email = jscfg["to_email"]
    password = jscfg["password"]

    df = pran.read_price_data()
    df_cheapest = pran.cheapest_history(df, 1)
    df_cheapest = pran.add_moving_avg(df)
    df_cheapest = df_cheapest.sort_values(by="diff_to_desired")

    df_cheapest["desired_price"] = round(df_cheapest["desired_price"], 2)
    df_cheapest["price_usd"] = round(df_cheapest["price_usd"], 2)
    df_cheapest["price_usd_SMA7"] = round(df_cheapest["price_usd_SMA7"], 2)
    df_cheapest["price_usd_SMA_delta"] = round(df_cheapest["price_usd_SMA_delta"], 2)

    df_output = df_cheapest[["card_name",
                               "set_name",
                               "collector_num",
                               "desired_price",
                               "price_usd",
                               "price_usd_SMA7",
                               "price_usd_SMA_delta",
                               "tcgplayer_uri"]].copy(deep=True)
    cols = {"card_name": "Card Name",
            "set_name": "Set Name",
            "collector_num": "Collector Number",
            "desired_price": "Desired Price",
            "price_usd":"Current Price",
            "price_usd_SMA7":"7-day Average Price",
            "price_usd_SMA_delta":"Current Price to 7-day Price Difference",
            "tcgplayer_uri":"TCG Player Link"}
    df_output.rename(columns=cols, inplace=True)
    df_html = df_output.to_html(index=False, justify="center")

    n_desired = df_cheapest.count()["tcgplayer_uri"]
    n_total = df_cheapest.shape[0]

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(from_email, password)

        # sending a fancier email
        mail = MIMEMultipart('alternative')
        mail['Subject'] = f'MTG Price Watcher Report for {date}'
        mail['From'] = from_email 
        mail['To'] = to_email

        html_template = f"""
        <i>sent @ {time}</i>
        <br>
        """

        html_template += f"You are currently watching <b>{n_total}</b> cards and <b>{n_desired}</b> are below desired price."
        html_template += df_html

        html_content = MIMEText(html_template, 'html')

        mail.attach(html_content)

        # Add any attachments in the directory
        for img in os.listdir("images"):
            mail = attach_file(f"images/{img}", mail)


        server.sendmail(from_email, to_email, mail.as_string())





if __name__ == "__main__":
    main()