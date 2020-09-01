# for email:
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders
from email_credentials import password, sender_email
import templates as html_templates
import yaml
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

def prepend(html_data, header): 
      
    # Using format() 
    header += '{0}'
    html_data = [header.format(i) for i in html_data] 
    return(html_data) 


def generate_report(figure_list, title_list, caption_list, fileName='Final.html', template='basic_theme.yaml'):
    """ Takes list of figures, titles, and captions to make an html report

    Args:
        figure_list (list):
        title_list (list):
        caption_list(list):
        filename (str): name of html file - default is 'Final.html'

    Returns:
        writes an html file
    """
    with open('templates/'+template) as file:
        template_dict = yaml.safe_load(file)

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

    file = open(fileName,"w+")
    file.write(html_template.format(here_html, css))
    file.close()  
    
    file2 = open(fileName, "r")
    html2 = file2.read()
    file2.close()   
        
    return html2

def embed_email(rec_email, report, text=" ", message = MIMEMultipart(), fileName = 'Final.html', del_files="no", subject="Email Report"):
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

        if os.path.exists("figures.html"):
            os.remove("figures.html")
        else:
            pass
            
        if os.path.exists(fileName):
            os.remove(fileName)
        else:
            pass
        
    else:
        pass
    return final_message


