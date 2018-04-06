#/usr/bin/env python

import smtplib
from email.mime.text import MIMEText
from email.parser import Parser
import requests
import json
from pprint import pprint
import configparser

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')

    with open('mail_headers.txt') as fp:
        headers = Parser().parse(fp)

    r = requests.get( 'https://api.github.com/search/issues?q={}'.format(config['github']['query']),
                      auth=(config['github']['user'], config['github']['password']))
    print("{}".format(r.status_code))


    message_body = "GitHub status : {}".format(r.status_code)


    if r.status_code == 200:

        github_response = json.loads(r.text)

        message_subject = headers['Subject'].format(github_response['total_count'])
        message_body += '\n------Issues------\n'

        for item in github_response['items']:

            print("{}\n#{} {}\n".format(item['html_url'],
                                  item['number'],
                                  item['title']))
            message_body += '#{}-{} ({})\n'.format(item['number'],
                                                   item['title'],
                                                   item['html_url'])




    else:
        message_subject = "GitHub request failed!"
        message_body = r.text


    msg = MIMEText(message_body)
    msg['To'] = headers['To']
    msg['From'] = headers['From']

    msg['Subject'] = message_subject

    s = smtplib.SMTP(config['general']['mail_server'])

    s.send_message(msg)
    s.quit()

