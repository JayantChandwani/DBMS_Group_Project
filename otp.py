import smtplib
import random
from savedata import *

otp = ''.join([str(random.randint(0,9)) for i in range(4)])

def send_otp(email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Replace with your Gmail address and app password
    sender_email = "ishug04112005@gmail.com"  
    app_password = "ufac ghdi mldx dkgy"
    
    server.login(sender_email, app_password)
    message = f"""From: {sender_email}
    To: {email}
    Subject: OTP

    Your OTP is: {otp}"""

    server.sendmail(sender_email, email, message)
    update_file(False, otp)
    server.quit()

