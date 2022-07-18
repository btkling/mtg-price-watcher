import pandas as pd
import price_analysis as pran
import smtplib 
import ssl
import json
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
        # server.sendmail(email, email, f"Subject: HELLO!\nBody of email.\n I am a test.")

        # sending a fancier email
        mail = MIMEMultipart('alternative')
        mail['Subject'] = 'Test HTML Message'
        mail['From'] = email 
        mail['To'] = email

        html_template = f"""
        <h1>I am the top level header</h1>
        <h2>I am a lower level header</h2>
        <p>{email} has sent me this message</p>
        """

        html_content = MIMEText(html_template, 'html')

        mail.attach(html_content)

        # Add an attachment
        mail = attach_file("images/image.png", mail)
        mail = attach_file("images/image2.png", mail)

        server.sendmail(email, email, mail.as_string())





if __name__ == "__main__":
    main()