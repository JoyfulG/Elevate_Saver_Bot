import time

import keyboard
import requests
import winsound

import message_body as mb
from elevate_saver_bot import send_message

session = requests.Session()
auth_token = mb.get_auth_token(session)
mb.payload['authenticity_token'] = auth_token

time.sleep(2)

session.post(mb.login_url, headers=mb.headers, data=mb.payload)  # Logging in

time.sleep(3)

print('READY')

while True:
    keyboard.wait('Left+Right')
    try:
        ticket_url = mb.url_grabber()
        last_comment = mb.last_internal_note_parser(session, ticket_url)
        winsound.PlaySound('url_captured.wav', winsound.SND_FILENAME)
        telegram_message = f'{ticket_url}\n{last_comment}'
    except IndexError:
        telegram_message = 'ERROR.\nProbably, ticket conversation is too long.'
    except AttributeError:
        telegram_message = 'ERROR.\nPlease make sure your active Chrome tab is a Zendesk ticket.\nIf everything ' \
                           'seems to be correct, restart "main".'
    except requests.exceptions.ConnectionError:
        telegram_message = 'ERROR.\nPlease make sure a URL in Chrome address line does NOT start with "https://".'
    send_message(telegram_message)
