"""
basic way to test reporty
"""

from R import send_email, embed_report, generate_page

sender_email = 'test.email.12700@gmail.com' 
password = 'testemail999OP!'

rec_email = 'deepkernel1@gmail.com'

image = 'images'

report = generate_page(image)
embed = embed_report(report, dir_name)
send_email(sender_email, password, rec_email, embed)
