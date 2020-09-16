from email_report import connect_email, send_email, embed_email, generate_report
from email_credentials import password, sender_email

# end user owns this function
from pandas import DataFrame
import numpy as np
from matplotlib import pyplot as plt
import random 
number = random.randint(1, 100000)

def make_random_figure():
    data =  np.random.normal(size=(20, 2))
    df = DataFrame(data, columns=['Goldfish Sales','Stock_Index_Price'])
    df['Stock_Index_Price'] += 10
    return df

rec_email = "deepkernel1@gmail.com"

if __name__ == "__main__":

    figure_list = [make_random_figure() for i in range(5)]
    title_list = ['a', 'b', 'c', 'd']
    caption_list = ['aa', 'bb', 'cc', 'dd']
    
    report = generate_report(figure_list, title_list, caption_list, template='green_theme.yaml', fileName ='myfile.html')
    embed = embed_email(rec_email, report, text="This message was sent with python", subject=str(number),  del_files='yes', fileName ='myfile.html')
    server = connect_email(sender_email, password)
    send_email(server, rec_email, embed)
    
