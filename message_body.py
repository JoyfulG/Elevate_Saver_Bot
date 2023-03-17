import json
import re

from pywinauto import Desktop
from bs4 import BeautifulSoup

import config

login_url = config.subdomain_login_url
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/108.0.0.0 Safari/537.36'}
payload = {
    'user[email]': config.login_email,
    'user[password]': config.login_pwd,
    'authenticity_token': ''
}


def url_grabber():
    chrome = Desktop(backend='uia').windows(title_re='.* Google Chrome$')[0]
    url_line = chrome.descendants(title='Адресная строка и строка поиска')[0]
    url = 'https://' + url_line.get_value()
    return url


def get_auth_token(session):
    login_code = session.post(login_url, headers=headers)
    login_soup = BeautifulSoup(login_code.text, 'lxml')
    token = login_soup.find('meta', {'name': 'csrf-token'}).get('content')
    return token


def last_internal_note_parser(session, ticket_url):
    ticket_code = session.get(ticket_url)
    ticket_soup = BeautifulSoup(ticket_code.text, 'lxml')
    convo_script = ticket_soup.find('script', {'data-preload-id': re.compile('conversations.json')})
    json_convo_dict = json.loads(convo_script.string)
    comment_text = ''

    for message in json_convo_dict['conversations']:
        if message['public'] is False:
            comment_text = message['body']
            break

    return comment_text
