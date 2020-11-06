"""
basic way to test reporty
"""

from reporty import send_email, embed_report, generate_report

sender_email = '' 
password = ''

rec_email = ''

from pandas import DataFrame
import numpy as np

def make(c, c2):
	data = np.random.normal(size=(20,2))
	df = DataFrame(data, columns=[c, c2])
	df[c2] += 10
	return d_f

fig_list = []
for i in range(10):
	fig = make_random_figure("Bros", "bros")
	fig_list.append(fig)

report = generate_report(fig_list)
embed = embed_report(report)
send_email(sender_email, password, rec_email, embed)

