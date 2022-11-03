from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
import smtplib, ssl, os
from dotenv import load_dotenv

load_dotenv()
sender = os.getenv('MY_GMAIL')
receiver = os.getenv('MY_GMAIL')
password = os.getenv('PASSWORD')
port = 587
smtp_server = 'smtp.gmail.com'
context = ssl.create_default_context()

# Create a multipart message and set headers
subject = "Internship - scraping Hellowork"
message = MIMEMultipart()
message["From"] = sender
message["To"] = receiver
message["Subject"] = subject

# Add body to email
body = 'Hello Elie<br/><br/><p>This is your daily update, enjoy it!</p><br/><hr/>'
message.attach(MIMEText(body, "html"))

filename = "results.json"

# Open file in binary mode
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
server = smtplib.SMTP(smtp_server, port)
try:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender, password)
    server.sendmail(sender, receiver, text)
except Exception as e:
    print(e)
finally:
    server.quit()