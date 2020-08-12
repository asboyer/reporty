# for email:
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders
from email_credentials import password, sender_email


# data 
import pandas as pd
from pandas import DataFrame 
import numpy
import matplotlib.pyplot as plt
from data import stockData as Data

# extra
import random
number = random.randint(1, 1000000)

# deleting files
import os

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
    print("Login success!")

    return server

    
def send_email(server, rec_email, message):
    # sends email
    server.sendmail(sender_email, rec_email, message)
    print("Email has been sent to " + rec_email)
    server.quit()


# for data
def make_random_figure():
    df = DataFrame(Data, columns=['Unemployment_Rate','Stock_Index_Price'])
    return df

def prepend(html_data, header): 
      
    # Using format() 
    header += '{0}'
    html_data = [header.format(i) for i in html_data] 
    return(html_data) 
    
# email stuff
rec_email = "deepkernel1@gmail.com"
message = MIMEMultipart()
message["Subject"] = str(number)
message["From"] = sender_email
message["To"] = rec_email


css = """
    body {
      background-color: linen;
    }
    
    h1 {
      color: maroon;
      margin-left: 0px;
    }
    """

html_template = """ 
<!DOCTYPE html>
<html>
<head>
<style>
{1}
</style>
</head>
<body>
{0}
</body>
</html>
    """

if __name__ == "__main__":
    
    # the text portion of the message
    text = "Here are some attatchments sent using Python!"
    message.attach(MIMEText(text, 'plain'))
    attatchment_amount = 8
    
    data_html = []
    figures_html = "figures.html"
    # creates the html file, converts into into text
    
    for i in range(attatchment_amount):
        fig = make_random_figure()
        fig.to_html(figures_html)
        f = open(figures_html,"r")
        html_fig = f.read()
        data_html.append(html_fig)
        f.close()

    header = """
    <h1>Your Figures:</h1>
    <p>Here are the figures upon request.</p>
        
    """
    newData = prepend(data_html, header)
        
    here_html = '\n'.join(newData)
    
    fileName = 'Final.html'
    file = open(fileName,"w+")
    file.write(html_template.format(here_html, css))
    file.close()  
    
    file2 = open(fileName, "r")
    html2 = file2.read()
    file2.close()    

    
    # converts html text into an embed in the email
    attatchment = MIMEText(html2, "html")
    message.attach(attatchment) 
    
    # html as attatchment
    attach_file = open(fileName, 'rb')
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload(attach_file.read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Disposition', 'attachment', filename=fileName)
    message.attach(payload)
    attach_file.close()
    
    # sends the email
    server = connect_email(sender_email, password)
    rec_email = 'deepkernel1@gmail.com'
    send_email(server, rec_email, message.as_string())
    
    # delete file
    if os.path.exists(fileName):
        os.remove(fileName)
    else:
        pass

    # delete file
    if os.path.exists(figures_html):
        os.remove(figures_html)
    else:
        pass