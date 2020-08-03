import smtplib
from email_credentials import password, sender_email


def connect_email(sender_email, password):
    """ sets up a smtp server
    Args:
        sender_email (str): senders email address
        password (str): password for sender's email

    Returns:
        smtplib.SMTP object
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success")

    return server


def send_email(server, rec_email, message):
    """ Sends email

    """
    server.sendmail(sender_email, rec_email, message)
    print("Email has been sent to ", rec_email)


if __name__ == "__main__":
    server = connect_email(sender_email, password)
    rec_email = 'asboyer@gmail.com'
    message = 'hello world'
    send_email(server, rec_email, message)
