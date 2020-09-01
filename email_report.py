# for email:
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders
from email_credentials import password, sender_email
import templates as html_templates
import yaml

# data 
import pandas as pd
from pandas import DataFrame 
import numpy as np
import matplotlib.pyplot as plt

# misc
import random

# deleting files
import os

# scheduling
import datetime as dt 
import time

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
    #print("Email has been sent to " + rec_email)
    server.quit()

    
def send_email_at(send_time, rec_email, server, message):
    time.sleep(send_time.timestamp() - time.time())
    send_email(server, rec_email, message.as_string())
    print("Email has been sent to " + rec_email)

first_email_time = dt.datetime(2020,8,18,14,23,45) # set this using millitary time
interval = dt.timedelta(minutes=1)
send_time = first_email_time

# for data
def make_random_figure():
    data =  np.random.normal(size=(20, 2))
    df = DataFrame(data, columns=['Goldfish Sales','Stock_Index_Price'])
    df['Stock_Index_Price'] += 10
    return df

def prepend(html_data, header): 
      
    # Using format() 
    header += '{0}'
    html_data = [header.format(i) for i in html_data] 
    return(html_data) 


def generate_report(figure_list, title_list, caption_list, filename='Final.html', template=None):
    """ Takes list of figures, titles, and captions to make an html report

    Args:
        figure_list (list):
        title_list (list):
        caption_list(list):
        filename (str): name of html file - default is 'Final.html'

    Returns:
        writes an html file
    """
    with open('templates/basic_theme.yaml') as file:
        template_dict = yaml.load(file)

    html_template = template_dict['html_template']
    header = template_dict['header']
    css = template_dict['css']
    
    data_html = []
    figures_html = "figures.html"
    # creates the html file, converts into into text
    
    for fig, title, caption in zip(figure_list, title_list, caption_list):
        fig.to_html(figures_html)
        f = open(figures_html,"r")
        html_fig = f.read()
        data_html.append(html_fig)
        f.close()

    
    newData = prepend(data_html, header)
        
    here_html = '\n'.join(newData)
    
    fileName = 'Final.html'
    file = open(fileName,"w+")
    file.write(html_template.format(here_html, css))
    file.close()  

    
# email stuff
rec_email = "deepkernel1@gmail.com"
message = MIMEMultipart()
message["Subject"] = 'hi'
message["From"] = sender_email
message["To"] = rec_email


if __name__ == "__main__":
    # while True:
    number = random.randint(1, 1000000)
    fig = make_random_figure()
    plt.show()
    # the text portion of the message
    text = "Check this out"
    message.attach(MIMEText(text, 'plain'))
    
    attatchment_amount = 3
    fig_list = []
    title_list = []
    caption_list = []
    for i in range(attatchment_amount):
        fig_list.append(make_random_figure())
        title_list.append('title {}'.format(i))
        caption_list.append('caption {}'.format(i))
    
    
    generate_report(fig_list, title_list, caption_list)

    # file2 = open(fileName, "r")
    # html2 = file2.read()
    # file2.close()    

    
    # # converts html text into an embed in the email
    # attatchment = MIMEText(html2, "html")
    # message.attach(attatchment) 
    
    # # html as attatchment
    # attach_file = open(fileName, 'rb')
    # payload = MIMEBase('application', 'octate-stream')
    # payload.set_payload(attach_file.read())
    # encoders.encode_base64(payload) #encode the attachment
    # #add payload header with filename
    # payload.add_header('Content-Disposition', 'attachment', filename=fileName)
    # message.attach(payload)
    # attach_file.close()
    
    # # sends the email
    # server = connect_email(sender_email, password)
    # send_email_at(send_time, rec_email, server, message)
    # send_time = send_time + interval
    # # send_email(server, rec_email, message.as_string())
    
    # # delete file
    # if os.path.exists(fileName):
        # os.remove(fileName)
    # else:
        # pass

    # # delete file
    # if os.path.exists(figures_html):
        # os.remove(figures_html)
    # else:
        # pass
