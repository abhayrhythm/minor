# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
msg={}

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'Tacsdc'
msg['From'] = 'uj00007@gmail.com'
msg['To'] = 'rhythmnarang25@gmail.com'

# Send the message via our own SMTP server.
s = smtplib.SMTP('smtp.gmail.com')
s.send_message(msg)
s.quit()