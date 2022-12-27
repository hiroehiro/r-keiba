import os
import random
import time
import tempfile
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from password import *

def wait(sleep_time=2):
    time.sleep(sleep_time+random.random()*1.5)

def switch_window(driver, original_window):
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

def create_message(subject, body, bcc_addrs=""):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    print(type(msg))
    return msg
 
def send(msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
    smtpobj.starttls()
    smtpobj.login(from_address, app_password)
    smtpobj.sendmail(from_address, to_address, msg.as_string())
    smtpobj.close()