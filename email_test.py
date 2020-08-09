import smtplib
from email_credentials import password, sender_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from pandas import DataFrame 
import numpy
import matplotlib.pyplot as plt



f = open("test_this.html","w+")
def make_random_figure():
    """ Makes a random figure (using pandas)

    Returns a matplotlib figure
    """
    

    # make some fake data or use numpy to get random data
    # Corona cases and deaths in MASS
    
    # how would I include dates?
    Data = {'Cases' : [0,1017,2033,4946,2106,1045,3840,101,23,428],
            'Death': [0,15,100,152,177,90,179,35,210,17]
    }
    # or get some real data from here https://pandas-datareader.readthedocs.io/en/latest/

    # pull data into a dataframe
    df = DataFrame(Data,columns=['Death','Cases'])
    # fig = df.plot()
    # fig = df.plot(x ='Death', y='Cases', kind = 'scatter')
    # return fig
    # return fig 
    return df
    
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


def send_email(server, rec_email, msg):
    """ Sends email

    """
    server.sendmail(sender_email, rec_email, message)
    print("Email has been sent to " + rec_email)


if __name__ == "__main__":
    fig = make_random_figure()
    fig.to_html('test_this.html')
    html = f.read()
    server = connect_email(sender_email, password)
    rec_email = 'deepkernel1@gmail.com'
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = rec_email
    msg = MIMEText(html, 'html')
    message.attach(msg)
    send_email(server, rec_email, message)
