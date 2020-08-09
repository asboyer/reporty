# for email:
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_credentials import password, sender_email

# data 
import pandas as pd
from pandas import DataFrame 
import numpy
import matplotlib.pyplot as plt
from data import stockData

def connect_email(sender_email, password):
    """ sets up a smtp server
    Args:
        sender_email (str): senders email address
        password (str): password for sender's email
    Returns:
        smtplib.SMTP object
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success")

    return server

    
def send_email(server, rec_email, message):
    # sends email
    server.sendmail(sender_email, rec_email, message)
    print("Email has been sent to " + rec_email)
    server.quit()


# for data
def make_random_figure():
    df = DataFrame(stockData,columns=['Unemployment_Rate','Stock_Index_Price'])
    return df

# email stuff
rec_email = "deepkernel1@gmail.com"
message = MIMEMultipart("alternative")
message["Subject"] = "subject"
message["From"] = sender_email
message["To"] = rec_email

if __name__ == "__main__":
    
    # creates the html file, converts into into text
    fig = make_random_figure()
    fig.to_html('test_this.html')
    f = open("test_this.html","r")
    html = f.read()
    text = "If you can see this message, my HTML did not send correctly!"
    
    # converts html text into an embed in the email
    textTo = MIMEText(text, 'plain')
    attatchment = MIMEText(html, "html")
    message.attach(textTo)
    message.attach(attatchment)
    
    # sends the email
    server = connect_email(sender_email, password)
    rec_email = 'deepkernel1@gmail.com'
    send_email(server, rec_email, message.as_string())

