"""
basic way to test reporty
"""

from R import send_email, embed_report, generate_report

sender_email = 'test.email.12700@gmail.com' 
password = 'testemail999OP!'

rec_email = 'deepkernel1@gmail.com'

from pandas import DataFrame
import numpy as np
from matplotlib import pyplot as plt

def make(c, c2):
	data = np.random.normal(size=(20,2))
	df = DataFrame(data, columns=[c, c2])
	df[c2] += 10
	return df

fig_list = []
for i in range(10):
	fig = make("Bros", "bros")
	fig_list.append(fig)
fig1, ax1 = plt.subplots(1, 1, figsize=(10, 5))
ax1.plot([1, 2, 3, 4, 5], [1, 4, 2, 4, 1])
fig2, ax2 = plt.subplots(1, 1, figsize=(10, 5))
ax2.plot([1, 2, 3, 4, 5], [2, 2, 2, 2, 3])
fig_list.append(fig1)
fig_list.append(fig2)

report = generate_report(fig_list)
embed = embed_report(report)
send_email(sender_email, password, rec_email, embed)


