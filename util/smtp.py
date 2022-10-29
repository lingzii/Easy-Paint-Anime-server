from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path
import smtplib

def sendEmail(to, img):
    content = MIMEMultipart()
    content["subject"] = "Easy Paint Anime!"
    content["from"] = "EPA! Work Team"
    content["to"] = to
    content.attach(MIMEImage(Path(img).read_bytes()))

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("08360716@me.mcu.edu.tw", "oxqnefmwnrzaajwb")
            smtp.send_message(content)
            print("Send Email Complete!")

        except Exception as e:
            print("Error message: ", e)