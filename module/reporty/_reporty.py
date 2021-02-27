"""
reporty contains a set of functions that will take figures and titles and generate
a full html report with those figures from selected templates

reporty also has functions that can embed this report in an email and send it out

docs: https://github.com/asboyer2/reporty/tree/master/docs
"""
import smtplib as _smtplib
import os as _os
from os import path as _path
import base64 as _base64
from io import BytesIO as _BytesIO
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.text import MIMEText as _MIMEText
from email.mime.image import MIMEImage as _MIMEImage
from email.mime.base import MIMEBase as _MIMEBase
from email import encoders as _encoders

import yaml as _yaml

# specifies path to templates
_TEMPLATES_DIR = _path.join(_path.dirname(__file__), 'templates')

# usable functions
__all__ = ['generate_report', 'generate_page', 'embed_report', 'send_email']

def generate_report(figure_list, title_list=0, caption_list=0,
                    file_name='reporty', template='basic',
                    alt_text=''):
    """ Takes list of figures, titles, captions,
     and a template to make an html report
    Makes an html file and turns possible matplot figures to png format,
     and makes a filenames text document

    Args:
        figure_list List[figures]: list of figures (matplot or dataframe)
        title_list List[str]: title of figure - default is "Figure" +
        figure number (ex: "Figure 1")
        caption_list List[str]: caption under title - default is "Caption" +
        figure number (ex: "Caption 1")
        file_name (str): name of html file - default is 'reporty'
        template (str): name of template - default is 'basic'
        alt_text (str): alt text for images - default is ''

    Returns:
        html file contents
    """
    # associates template input with respective yaml file
    template = template + "_theme.yaml"

    # takes custom file name and adds html file extension
    file_name = file_name + ".html"

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
    with open(_TEMPLATES_DIR + '/' + template) as file:
        template_dict = _yaml.safe_load(file)
    html_template = template_dict['html_template']
    header_template = template_dict['header']
    css = template_dict['css']
    image = template_dict['image']
    image_data = template_dict['image_data']

    # creates empty lists
    data_html = []
    header_html = []
    matplot_count = []
    matplot_names = []

    # creates the html file, converts into into text
    # get list of figure html
    for fig, title, caption in zip(figure_list, title_list, caption_list):
        # html_fig = fig.to_html()
        if str(fig.__class__) == "<class 'matplotlib.figure.Figure'>":
            matplot_count.append("r")
            matplot_names.append(_matplot_png(fig, file_name, matplot_count))
        else:
            pass
        # turns figures into html
        data_html.append(_make_html_from_figure_object(fig, alt_text,
                                                       matplot_names, image,
                                                       image_data))
        # get list of header & captions html
        header_html.append(header_template.format(title=title, caption=caption))

    # writes correct file names for matplot png
    if len(matplot_names) > 0:
        file = open("filenames.txt", "w+")
        my_string = (str(matplot_names)).replace("'", '')
        file.write(my_string)
        file.close()

    # puts respective headers in front of respective data
    new_data = _prepend(data_html, header_html)

    # creates html with all of the new data joined together by a line break
    here_html = '\n'.join(new_data)

    # makes html file and uses template and formats the html and css
    file = open(file_name, "w+")
    file.write(html_template.format(here_html, css))
    file.close()

    # takes contents of html file and puts them into 'html2' variable
    file2 = open(file_name, "r")
    html2 = file2.read()
    file2.close()

    # returns (str) 'html2' with html files contents
    return html2

def generate_page(images, title_list=0, caption_list=0,
                    file_name='reporty', template='basic',
                    alt_text='', dir_name=''):
                    
    # associates template input with respective yaml file
    template = template + "_theme.yaml"

    # takes custom file name and adds html file extension
    file_name = file_name + ".html"
    image_names = []
    dir_name = 0

    if type(images) == list:
        for img in images:
            image_names.append(_png_name(img))
            images = image_names
    elif type(images) == str:
        dir_name = images
        files = _os.listdir(images)
        images = []
        for f in files:
            images.append(f)
    else:
        raise Exception('''Invalid - must be a list of images or file path 
                        to dir with images''')
    
    # writes default captions
    if title_list == 0:
        title_list = []
        for i in range(len(images)):
            title_list.append("Figure "+str(i+1))
    else:
        pass

    if caption_list == 0:
        caption_list = []
        for i in range(len(images)):
            caption_list.append("Caption "+str(i+1))
    else:
        pass

    while len(title_list) < len(images):
        title_list.append("Default Title")

    while len(caption_list) < len(images):
        caption_list.append("Default Caption")

    # loads specified template yaml file and assigns parts as variables
    with open(_TEMPLATES_DIR + '/' + template) as file:
        template_dict = _yaml.safe_load(file)
    html_template = template_dict['html_template']
    header_template = template_dict['header']
    css = template_dict['css']
    image = template_dict['image']
    image_data = template_dict['image_data']
    
    # creates empty lists
    image_html = []
    header_html = []
    

    for img, title, caption in zip(images, title_list, caption_list):
        image_html.append(_make_html_from_png(img, alt_text, image, image_data, dir_name))
        header_html.append(header_template.format(title=title, caption=caption))
        
    file = open("filenames.txt", "w+")
    if dir_name == 0:
        my_string = (str(image_names)).replace("'", '')
    else:
        my_string = (str(images)).replace("'", '')
    file.write(my_string)
    file.close()
    
    new_data = _prepend(image_html, header_html)

    # creates html with all of the new data joined together by a line break
    here_html = '\n'.join(new_data)

    # makes html file and uses template and formats the html and css
    file = open(file_name, "w+")
    file.write(html_template.format(here_html, css))
    file.close()

    # takes contents of html file and puts them into 'html2' variable
    file2 = open(file_name, "r")
    html2 = file2.read()
    file2.close()

    # returns (str) 'html2' with html files contents
    return html2

def embed_report(report, file_name='reporty', del_files='no',
                 subject='', sender_name='', rec_name='', text='', dir_name=0):
    """ embeds report in custom email, and attaches html files and pngs

    Args:
        report (str): html code
        filename (str): name of html file (if you entered a custom file name in
        'generate report', you must pass that filename through in this function)
        - default is 'reporty'
        del_files (str): 'yes' will delete files - default is 'no' (keep files)
        subject (str): subject of email - default is '' (no subject)
        sender_name (str): name of sender (will be email name no matter what on
        outlook) - default is '' (will result to email address on all platforms)
        rec_name (str): name of receiver (must be left blank for outlook users)
        - default is '' (will result in no send tag for gmail)
        text (str): any extra text you want to send will appear at start of
        email - default is '' (will result to no extra text)

    Returns:
        encoded multipart message
    """

    # declaring message object
    message = _MIMEMultipart()

    # takes custom file name and adds html file extension
    file_name = file_name + ".html"

    # declaring empty file names list
    file_names = []

    # takes filenames from
    if _os.path.exists("filenames.txt"):
        file = open("filenames.txt", "r")
        filenames = file.read()
        file.close()
        _os.remove("filenames.txt")
        file_names = filenames.strip('][').split(', ')
    else:
        pass

    # adds a sender_name, receiver name, and a subject
    if sender_name == '':
        pass
    elif not(" " in sender_name.strip()):
        sender_name = sender_name.strip() + ' (via reporty)'
        message["From"] = str(sender_name)
    else:
        message["From"] = str(sender_name).strip()
    if rec_name == '':
        pass
    else:
        rec_name = (str(rec_name)).replace(" ", "_")
        message["To"] = rec_name
    if subject == '':
        pass
    else:
        message["Subject"] = str(subject)

    # attatches 'text' to message
    message.attach(_MIMEText(text, 'plain'))

    # attatches the html attachment to message
    attachment = _MIMEText(report, "html")
    message.attach(attachment)

    # adds a content id to all matplot pngs and attaches images
    if len(file_names) > 0:
        for i in range(len(file_names)):
            if dir_name == 0:
                f_p = open(file_names[i], 'rb')
            else:
                f_p = open(dir_name + '/' + file_names[i], 'rb')
            image = _MIMEImage(f_p.read(), filename=file_names[i])
            _encoders.encode_base64(image)
            f_p.close()
            image.add_header('Content-ID', '<' + file_names[i].replace('.png', '') + '>')
            image.add_header('Content-Disposition', 'inline', filename=file_names[i])
            message.attach(image)
    else:
        pass

    # opens the html file and adds 'payload'
    attach_file = open(file_name, 'rb')
    payload = _MIMEBase('application', 'octate-stream')
    payload.set_payload(attach_file.read())

    # encodes payload
    _encoders.encode_base64(payload)

    # add payload header with filename
    payload.add_header('Content-Disposition', 'attachment', filename=file_name)

    # attatches html file to the email
    message.attach(payload)
    attach_file.close()

    # creates final message (str)
    final_message = message.as_string()

    # deletes extra files if user specifies
    if del_files == 'yes':
        if _os.path.exists(file_name):
            _os.remove(file_name)
        else:
            pass
        for i in range(len(file_names)):
            if _os.path.exists(file_names[i]):
                _os.remove(file_names[i])
    else:
        pass

    # returns the mime multipart message (str)
    return final_message

def send_email(sender_email, password, rec_email, message):
    """ connects sender to server and calls _sent_email() function
    Args:
        sender_email (str): senders email address
        password (str): password for sender's email
        rec_email (str): receiver's email
        message (str): attached message

    Returns:
        passes smtplib.SMTP object through _sent_email() function to send email
    """

    # connecting to outlook smtp server, then defaults to gmail
    if sender_email.endswith("outlook.com"):
        server = _smtplib.SMTP('smtp-mail.outlook.com', 587)
    else:
        server = _smtplib.SMTP('smtp.gmail.com', 587)

    # connects email to server
    server.starttls()
    server.login(sender_email, password)
    print("Login success!")

    # calls second send email function
    _sent_email(server, rec_email, message, sender_email)

def _sent_email(server, rec_email, message, sender_email):
    """ sends email
    Args:
        server <smtplib.SMTP object>: smtplib.SMTP object
        rec_email (str): receiver's email
        message (str): attached message
        sender_email (str): senders email address
        password (str): password for sender's email

    Returns:
        sends email, prints confirmation and quits server
    """

    # sends email, prints confirmation and quits server
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

    # declares empty list
    full_html = []

    # replaces first item in one list with the first item in other list
    for data, header in zip(data_html, header_html):
        header += '{data}'
        single_figure_html = header.format(data=data)
        full_html.append(single_figure_html)

    # returns new list in correct order
    return full_html

def _matplot_png(fig, file_name, matplot_count):
    """ turns matplot fig to png and names image accordingly
    Args:
        fig (matplot figure): matplot figure passed through
        file_name (str): filename for the final html file - default is 'reporty'
        matplot_count List[str]: keeps track of amount of figures
    Returns:
        A list with each item a [header+data, header+data] ...
    """

    # creates filename based on number of matplot figures and filename
    f_name = file_name.replace('.html', '_figure{}.png'.format(len(matplot_count)))

    # saves fig as a png using the above created name
    fig.savefig(f_name)

    # returns the name of the created png
    return f_name

def _make_html_from_figure_object(fig, alt_text, matplot_names, image, image_data):
    """Turns a 'figure' into html

    Args:
        fig: either a pandas dataframe or a matplotlib figure object
        alt_text (str): alt text for html implementation
        matplot_names List[str]: list of matplot names
        image (str): content id html format from yaml template file
        image_data(str): embed image html format from yaml template file

    Returns:
        string of html

    """

    # checks if matplot fig
    if str(fig.__class__) == "<class 'matplotlib.figure.Figure'>":
        # generate the figure and save as png
        buf = _BytesIO()
        fig.savefig(buf, format="png")
        # embed the result in the html output
        data = _base64.b64encode(buf.getbuffer()).decode("ascii")
        html_string0 = ("\n" + image_data + "\n").format(data=data, alt_text=alt_text)
        for i in range(len(matplot_names)):
            html_string1 = ("\n" + image + "\n").format(image=matplot_names[i].replace('.png', ''),
                                                        alt_text=alt_text)
        html_string = html_string1 + html_string0

    #TO DO: get rid of broken image icon

    # checks if dataframe
    elif str(type(fig)) == "<class 'pandas.core.frame.DataFrame'>":
        html_string = fig.to_html(border=0)

    # raises exception if unknown fig
    else:
        raise Exception('''Invalid figure object - must be a pandas
                        dataframe or a matplotlib figure object''')

    # html string from figure object
    return html_string

def _png_name(img):

    f_name = img + ".png"

    return f_name

def _make_html_from_png(img, alt_text, image, image_data, dir_name):
    if dir_name == 0:
        f = open(img, "rb")
        data = _base64.b64encode(f.read()).decode("ascii")
    else:
        f = open(dir_name + '/' + img, "rb")
        data = _base64.b64encode(f.read()).decode("ascii")
    html_string0 = ("\n" + image_data + "\n").format(data=data, alt_text=alt_text)
    html_string1 = ("\n" + image + "\n").format(image=img.replace('.png', ''),
                                                            alt_text=alt_text)
    html_string = html_string1 + html_string0
    f.close()
        
    return html_string
# Written by Andrew Boyer with help from Ben Tengleson
