"""
basic way to test reporty
"""

from R import send_email, embed_report, generate_page

image = 'images'

report = generate_page(image)
embed = embed_report(report, dir_name)
send_email(sender_email, password, rec_email, embed)
