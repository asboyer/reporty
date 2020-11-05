"""
A basic way to use the reporty functions while generating figures
"""

# import the three functions from reporty
from reporty import send_email, embed_report, generate_report

# import email credentials file, or assign variables (would not recommend for
#security reasons)
from email_credentials_template import sender_email, password

# import the functions necessary to create figures
from pandas import DataFrame
from matplotlib import pyplot as plt
import numpy as np

# receiver's email
rec_email = "your_email@gmail.com"

# function makes random figures
def make_random_figure(c_1, c_2):
    """ Creates random figures

    Args:
        c_1 (str): first column name
        c_2 (str): second column name

    Returns:
        dataframe with random data
    """

    data = np.random.normal(size=(20, 2))
    d_f = DataFrame(data, columns=[c_1, c_2])
    d_f[c_2] += 10
    return d_f

if __name__ == "__main__":

    # makes two matplots
    fig1, ax1 = plt.subplots(1, 1, figsize=(10, 5))
    ax1.plot([1, 2, 3, 4, 5], [1, 4, 2, 4, 1])
    fig2, ax2 = plt.subplots(1, 1, figsize=(10, 5))
    ax2.plot([1, 2, 3, 4, 5], [2, 2, 2, 2, 3])

    # makes two figures using above 'make_random_figure'
    fig3 = make_random_figure("Goldfish", "Bros")
    fig0 = make_random_figure("Students", "Scores")

    # list of the figures made
    figure_list = [fig0, fig1, fig2, fig3]

    # makes random captions and titles
    caption_list = ['caption ' + str(i) for i in range(5)]
    title_list = ['title ' + str(i) for i in range(5)]

# easy way to use functions:
# generates report with figures, caption, and titles
report = generate_report(figure_list, caption_list, title_list)
# embeds generated report in email
embed = embed_report(report)
# sends the email with credentials
send_email(sender_email, password, rec_email, embed)

# advanced way to use functions:
# generates report with figures, caption, titles, filename, template, and alt_text
# NOTE: to use custom file_name, it must be passed through generate and embed functions
report = generate_report(figure_list, caption_list, title_list,
                         file_name='my_file', template='green',
                         alt_text='figure')
# embeds generated report in email, custom file_name, deletes made files, attaches
#a custom subject to email, custom sender_name, custom receiver name, and extra text
# NOTE: custom receiver name does not currently function for sending outlook email addresses
embed = embed_report(report, file_name='my_file', del_files='yes',
                     subject='Your figures', sender_name='reporty',
                     rec_name='My Friend', text="your figures, sir")
# sends the email with credentials
send_email(sender_email, password, rec_email, embed)

# docs written by Andrew Boyer
