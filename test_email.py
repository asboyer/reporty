import smtplib

sender_email = input("Please enter your email: ")
password = input("Please enter your password : ")
rec_email = input("Please enter reciever email: ")


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)
print("Login success")

message = input("Enter your message to the reciever: ")
server.sendmail(sender_email, rec_email, message)
print("Email has been sent to ", rec_email)
