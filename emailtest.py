
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import email

from robot1 import *
from camera import *

user = 'flintwinters.0'
password = 'Kokonuts123'
fullAddress = user + "@gmail.com"
imap_url = 'imap.gmail.com'

con = imaplib.IMAP4_SSL(imap_url)
con.login(user, password)
con.select('INBOX')


def get_body(msg):
    try:
        if msg.is_multipart():
            return get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True).decode("utf-8")
    except:
        return ""


def getTopEmailBody():
    i = 1
    con.select('INBOX')
    while 1:
        raw, data = con.fetch(str.encode(str(i)), '(RFC822)')
        if data[0] is not None:
            i += 1
        else:
            raw, data = con.fetch(str.encode(str(i - 1)), '(RFC822)')
            raw = email.message_from_bytes(data[0][1])
            break
    return get_body(raw)


def sendImage(fileName=defaultImageName):
    print("Sending...")
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fullAddress, password)

    message = MIMEMultipart()
    message['From'] = fullAddress
    message['To'] = fullAddress

    takePic()
    with open(fileName, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        print("Encoding...")
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + fileName)
        print("Attaching image to email...")
        message.attach(part)
        text = message.as_string()
    print("Sending now...")
    server.sendmail(fullAddress, fullAddress, text)
    server.quit()
    print("Successfully returned image")

def executeInstruction(seconds, powerA=50, powerB=50):
    goTime(seconds, powerA, powerB)
    # sendImage()

GPIO.setup(18, GPIO.OUT)
try:
    while 1:
        GPIO.output(18, GPIO.LOW)
        
        topEmail = getTopEmailBody()
        if len(topEmail) > 1:
            direction = topEmail[0]
            seconds = int(topEmail[1])
            if direction == "w":
                executeInstruction(seconds, 50, -50)
            elif direction == "a":
                executeInstruction(seconds, 50, 50)
            elif direction == "d":
                executeInstruction(seconds, -50, -50)
            elif direction == "s":
                executeInstruction(seconds, -50, 50)
except:
    GPIO.output(18, GPIO.HIGH)
