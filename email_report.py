# for email:
import smtplib
import numpy as np
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders
from email_credentials import password, sender_email
import templates as html_templates
import yaml
import mpld3
from matplotlib import pyplot as plt
# deleting files
import os
import re
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import StringIO

# 
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

def prepend(data_html, header_html): 
      
    # Using format() 
    full_html = []
    for data, header in zip(data_html, header_html):
        # header += '{data}{caption}'
        header += '{data}'
        single_figure_html = header.format(data=data)
        full_html.append(single_figure_html)
 
    return(full_html) 


def matplot_png(fig, fileName, matplot_count):
    fileName = fileName.replace('.html','{}.png')
    png_list = []
    for i in range(len(matplot_count)+1):
        fileName = fileName.format("_" + str((i+1)))
        fig.savefig(fileName)
        png_list.append(fileName)
    return png_list

def make_html_from_figure_object(fig, alt_text):
    """Turns a 'figure' into html

    Args: 
        fig: either a pandas dataframe or a matplotlib figure object

    Returns:
        string of html

    """
    if str(fig.__class__) == "<class 'matplotlib.figure.Figure'>":
        import base64
        from io import BytesIO   
    
        #Generate the figure **without using pyplot**.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        html_string = "<div> \n <img src=\"data:image/png;base64,{data}\" alt=\"{alt_text}\" /> \n <div>".format(data=data, alt_text=alt_text)
        
        #this test works:
        #html_string = "<img src=\"https://blog.mailtrap.io/wp-content/uploads/2018/11/blog-illustration-email-embedding-images.png?w=640\" alt=\"img\" />"
        # check this out: https://www.campaignmonitor.com/blog/email-marketing/2019/04/embedded-images-in-html-email/
    elif str(type(fig)) == "<class 'pandas.core.frame.DataFrame'>":
        html_string = fig.to_html()
    
    else:
        raise Exception('Invalid figure object - must be a pandas dataframe or a matplotlib figure object')
    
    return html_string
        


def generate_report(figure_list, title_list=0, caption_list=0, fileName='Final.html', template='basic_theme.yaml', alt_text='Matplotlib figure'):
    """ Takes list of figures, titles, and captions to make an html report

    Args:
        figure_list (list):
        title_list (list):
        caption_list(list):
        filename (str): name of html file - default is 'Final.html'

    Returns:
        writes an html file
    """
    
    if title_list == 0:
        title_list = []
        for i in range (len(figure_list)):
            title_list.append("Figure "+str(i+1))
    else:
        pass
    
    if caption_list == 0:
        caption_list = []
        for i in range (len(figure_list)):
            caption_list.append("Caption "+str(i+1))
    else:
        pass

    while len(title_list) < len(figure_list):
        title_list.append("Default Title")
        
    while len(caption_list) < len(figure_list):
        caption_list.append("Default Caption")
            
    with open('templates/'+template) as file:
        template_dict = yaml.safe_load(file)

    html_template = template_dict['html_template']
    header_template = template_dict['header']
    css = template_dict['css']
    
    data_html = []
    header_html = []
    caption_html = []
    figures_html = "figures.html"
    # creates the html file, converts into into text
    
    for fig, title, caption in zip(figure_list, title_list, caption_list):
        # get list of figure html
        #html_fig = fig.to_html()
        matplot_count = []
        png_list = []
        if str(fig.__class__) == "<class 'matplotlib.figure.Figure'>":
            matplot_count.append("r")
        else:
            pass
        if str(fig.__class__) == "<class 'matplotlib.figure.Figure'>":
            matplot_png(fig, fileName, matplot_count)
            
        data_html.append(make_html_from_figure_object(fig, alt_text))

        # get list of header & captions html
        header_html.append(header_template.format(title=title, caption=caption))

    newData = prepend(data_html, header_html)
        
    here_html = '\n'.join(newData)

    file = open(fileName,"w+")
    file.write(html_template.format(here_html, css))
    file.close()  
    
    file2 = open(fileName, "r")
    html2 = file2.read()
    file2.close()   
        
    return html2

def embed_email(rec_email, report, text="Default text", message = MIMEMultipart(), fileName = 'Final.html', del_files="no", subject="Email Report"):
    message["From"] = sender_email
    message["To"] = rec_email
    message["Subject"] = subject
    message.attach(MIMEText(text, 'plain'))
    
    attatchment = MIMEText(report, "html")
    message.attach(attatchment) 
    
    attach_file = open(fileName, 'rb')
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload(attach_file.read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Disposition', 'attachment', filename=fileName)
    message.attach(payload)
    attach_file.close()
    
    final_message = message.as_string()
    if del_files == 'yes':
        if os.path.exists("Final.html"):
            os.remove("Final.html")
        else:
            pass
        if os.path.exists(fileName):
            os.remove(fileName)
        else:
            pass
    
    else:
        pass
    return final_message


def make_random_figure():
    data =  np.random.normal(size=(19, 2))
    df = pd.DataFrame(data, columns=['Goldfish Sales','Stock_Index_Price'])
    df['Stock_Index_Price'] += 9
    return df


if __name__ == "__main__":


    fig1, ax1 = plt.subplots(1,1, figsize=(10,5))
    ax1.plot([1,2,3,4,5], [1,4,2,4,1])

    fig2, ax2 = plt.subplots(1,1, figsize=(10,5))
    ax2.plot([1,2,3,4,5], [2,2,2,2,3])

    fig3 = make_random_figure()
    fig0 = make_random_figure()


    figure_list = [fig0, fig1, fig2, fig3]
    caption_list = ['caption' + str(i) for i in range(5)]
    title_list = ['title' + str(i) for i in range(5)]
 
    html_report = generate_report(figure_list, title_list=title_list, caption_list=caption_list, fileName='Final_plots.html', template='basic_theme.yaml')

