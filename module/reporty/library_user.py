from reporty import connect_email, send_email, embed_report, generate_report
from email_credentials import password, sender_email

# end user owns this function
from pandas import DataFrame
from matplotlib import pyplot as plt
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

    fig1, ax1 = plt.subplots(1,1, figsize=(10,5))
    ax1.plot([1,2,3,4,5], [1,4,2,4,1])
    

    fig2, ax2 = plt.subplots(1,1, figsize=(10,5))
    ax2.plot([1,2,3,4,5], [2,2,2,2,3])

    fig3 = make_random_figure()
    fig0 = make_random_figure()


    figure_list = [fig0, fig1, fig2, fig3]
    caption_list = ['caption ' + str(i) for i in range(5)]
    title_list = ['title ' + str(i) for i in range(5)]

    
report = generate_report(figure_list, title_list, caption_list, template='basic_theme', fileName ='myfile.html', alt_text='this text is just in case email is stupid')
embed = embed_report(rec_email, report, text="This message was sent with python", subject=str(number),  del_files='yes', fileName ='myfile.html')
server = connect_email(sender_email, password)
send_email(server, rec_email, embed, sender_email)
    