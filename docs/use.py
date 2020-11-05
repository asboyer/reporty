"""
two ways to use the reporty functions
"""

# !NOTE: this file only provides information on how to use reporty and
#it does not show how to use it in context: which is available at use_context.py

# import the three functions from reporty
from reporty import send_email, embed_report, generate_report

# import email credentials file, or assign variables (would not recomend for
#security reasons)
from email_credentials_template import sender_email, password

# receiver's email
rec_email = "your_email@gmail.com"

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
