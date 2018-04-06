#/usr/bin/env python

import os
import smtplib
from email.mime.text import MIMEText
from email.parser import Parser
import requests

if __name__ == '__main__':

    with open('mail_headers.txt') as fp:
         headers = Parser().parse(fp)
    msg = MIMEText("")
    msg['To'] = headers['To']
    msg['From'] = headers['From']

    msg['Subject'] = headers['Subject'].format(cumulative_percent)

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
