import smtplib as _smtplib
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.text import MIMEText as _MIMEText
from email.mime.image import MIMEImage as _MIMEImage
from email.mime.base import MIMEBase as _MIMEBase
from email import encoders as _encoders
import yaml as _yaml
import os as _os
from os import path as _path

_templates_dir = _path.join(_path.dirname(__file__), 'templates')
__all__ = ['generate_report', 'embed_report', 'send_email']

def generate_report(figure_list, title_list=0, caption_list=0,
                    fileName='reporty.html', template='basic',
                    alt_text=''):
    """ Takes list of figures, titles, captions,
     and a template to make an html report
    Makes an html file and turns possible matplot figures to png format,
     and makes a filenames text document

    Args:
        figure_list (list): list of figures (matplot or dataframe)
        title_list (list): title of figure - default is "Figure" +
        figure number (ex: "Figure 1")
        caption_list(list): caption under title - default is "Caption" +
        figure number (ex: "Caption 1")
        filename (str): name of html file - default is 'reporty.html'
        template (str): name of template - default is 'basic'
        alt_text (str): alt text for images - default is ''

    Returns:
        html file contents
    """
    # associates template input with respective yaml file
    template = template + "_theme.yaml"

    # writes default captions
    if title_list == 0:
        title_list = []
        for i in range(len(figure_list)):
            title_list.append("Figure "+str(i+1))
    else:
        pass

    if caption_list == 0:
        caption_list = []
        for i in range(len(figure_list)):
            caption_list.append("Caption "+str(i+1))
    else:
        pass

    while len(title_list) < len(figure_list):
        title_list.append("Default Title")

    while len(caption_list) < len(figure_list):
        caption_list.append("Default Caption")

    # loads specified template yaml file and assigns parts as variables
    with open(_templates_dir + '/' + template) as file:
        template_dict = _yaml.safe_load(file)
    html_template = template_dict['html_template']
    header_template = template_dict['header']
    css = template_dict['css']
    image = template_dict['image']
    image_data = template_dict['image_data']

    # creates empty lists
    data_html = []
    header_html = []
    caption_html = []
    matplot_count = []
    matplot_names = []

    # creates the html file, converts into into text
    # get list of figure html
    for fig, title, caption in zip(figure_list, title_list, caption_list):
        # html_fig = fig.to_html()
        if str(fig.__class__) == "<class 'matplotlib.figure.Figure'>":
            matplot_count.append("r")
            matplot_names.append(_matplot_png(fig, fileName, matplot_count))
        else:
            pass
        # turns figures into html
        data_html.append(_make_html_from_figure_object(fig, alt_text,
                                                       matplot_names, image,
                                                       image_data))
        # get list of header & captions html
        header_html.append(header_template.format(title=title, caption=caption))
    
    # writes correct filenames for matplot png
    if len(matplot_names) > 0:
        file = open("filenames.txt", "w+")
        my_string = (str(matplot_names)).replace("'", '')
        file.write(my_string)
        file.close()
    
    # puts respective headers in front of respective data
    newData = _prepend(data_html, header_html)
        
    # 
    here_html = '\n'.join(newData)

    file = open(fileName,"w+")
    file.write(html_template.format(here_html, css))
    file.close()  
    
    file2 = open(fileName, "r")
    html2 = file2.read()
    file2.close()   
        
    return html2
    
def embed_report(report, fileName = 'reporty.html', del_files='no', subject='', sender_name='', rec_name='me', text=''):
    
    message = _MIMEMultipart()
    fileNames = []
    if _os.path.exists("filenames.txt"):
        file = open("filenames.txt", "r")
        filenames = file.read()
        file.close()
        _os.remove("filenames.txt")
        fileNames = filenames.strip('][').split(', ')
    
    else:
        pass
        
    if sender_name == '':
        pass
    else:
        message["From"] = str(sender_name)
    if rec_name == '':
        pass
    else:
        rec_name = (str(rec_name)).replace(" ", "_")
        message["To"] = rec_name
    if subject == '':
        pass
    else:    
        message["Subject"] = str(subject)
        
    message.attach(_MIMEText(text, 'plain'))
    
    attatchment = _MIMEText(report, "html")
    message.attach(attatchment) 
    
    
    if len(fileNames) > 0:
        for i in range(len(fileNames)):
            fp = open(fileNames[i], 'rb')
            image = _MIMEImage(fp.read(), filename=fileNames[i])
            _encoders.encode_base64(image)
            fp.close()
            image.add_header('Content-ID', '<' + fileNames[i].replace('.png', '') + '>')
            image.add_header('Content-Disposition', 'inline', filename=fileNames[i])
            message.attach(image)
    else:
        pass
    attach_file = open(fileName, 'rb')
    payload = _MIMEBase('application', 'octate-stream')
    payload.set_payload(attach_file.read())
    _encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Disposition', 'attachment', filename=fileName)
    message.attach(payload)
    attach_file.close()
    
    final_message = message.as_string()
    if del_files == 'yes':
        if _os.path.exists("reporty.html"):
            _os.remove("reporty.html")
        else:
            pass
        if _os.path.exists(fileName):
            _os.remove(fileName)
        else:
            pass
        for i in range(len(fileNames)):
            if _os.path.exists(fileNames[i]):
                _os.remove(fileNames[i])
    else:
        pass
    return final_message

def send_email(sender_email, password, rec_email, message):
    """ sets up a smtp server
    Args:
        sender_email (str): senders email address
        password (str): password for sender's email
    Returns:
        smtplib.SMTP object
    """
    if sender_email.endswith("outlook.com"):
        server = _smtplib.SMTP('smtp-mail.outlook.com', 587)
    else:
        server = _smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success!")
    _sent_email(server, rec_email, message, sender_email, password)

def _sent_email(server, rec_email, message, sender_email, password):
    # sends email
    server.sendmail(sender_email, rec_email, message)
    print("Email has been sent to " + rec_email)
    server.quit()

def _prepend(data_html, header_html): 
    """ inserts header in front of data
    Args:
        data_html List[str]: list of html for each figure
        header_html List[str]: list of titles and captions for each figure
    Returns:
        A list with each item a [header+data, header+data] ...
    """
    full_html = []
    for data, header in zip(data_html, header_html):
        # header += '{data}{caption}'
        header += '{data}'
        single_figure_html = header.format(data=data)
        full_html.append(single_figure_html)
 
    return(full_html) 

def _matplot_png(fig, fileName, matplot_count):
    fileName = fileName.replace('.html','_matplot_figure{}.png'.format(len(matplot_count)))
    fig.savefig(fileName)
    return fileName

def _make_html_from_figure_object(fig, alt_text, matplot_names, image, image_data):
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
        #html_string0 = "<img src=\"data:image/png;base64,{data}\" /> \n ".format(data=data)
        html_string0 = ("\n" + image_data + "\n").format(data=data)
        for i in range(len(matplot_names)):
            html_string1 = ("\n" + image + "\n").format(image=matplot_names[i].replace('.png', ''))
        html_string = html_string1 + '\n' + html_string0
    
    #TO DO: get rid of broken image icon
    
    
    elif str(type(fig)) == "<class 'pandas.core.frame.DataFrame'>":
        html_string = fig.to_html(border=0)
    
    else:
        raise Exception('Invalid figure object - must be a pandas dataframe or a matplotlib figure object')
    
    return html_string        

# Written by Andrew Boyer and Ben Tengleson 
