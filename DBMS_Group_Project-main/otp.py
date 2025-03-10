import smtplib
import random
from savedata import *

otp = ''.join([str(random.randint(0,9)) for i in range(4)])

def send_otp(email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('d25385934@gmail.com', 'mfjymoirdwyzjdlh')
    message = """From: d25385934@gmail.com
    To:""" +  email  + """
    Subject: OTP

    Your OTP is  : """ + otp

    server.sendmail('d25385934@gmail.com', email, message)
    update_file(False, otp)
    server.quit()

