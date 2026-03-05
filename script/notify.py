# Klipper extension for Pushover notification
#
# Copyright (C) 2023  Rudy Dajoh <prd0000@gmail.com>
#
# This file may be distributed under the terms of the GNU AGPLv3 license.

import requests

HELP='''
Klipper Push Notification module for PushOver.
USAGE: PUSH_NOTIFY MSG="message" DEVICE="deviceid" [TITLE="title" SOUND="sound" PRIORITY=0 RETRY=30 EXPIRE=90]
DEVICE should be your device id in pushover.
TITLE, SOUND, PRIORITY, RETRY, and EXPIRE parameters are optional
PRIORITY can be between -2 and 2
RETRY must be greater than or equal to 30 if specified
EXPIRE must be between RETRY and 10800
'''

class Notify:
    def __init__(self, config) -> None:
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')

        # configuration
        self.api_key = config.get('api_key')
        self.user_key = config.get('user_key')
        self.timeout = config.get('timeout', 10)

        # Register commands
        self.gcode.register_command(
            "PUSH_NOTIFY", 
            self.cmd_PUSH_NOTIFY, 
            desc=self.cmd_PUSH_NOTIFY_help)

    cmd_PUSH_NOTIFY_help = "Sending message to pushover server"
    def cmd_PUSH_NOTIFY(self, params):
        message = params.get('MSG', '')
        device_id = params.get('DEVICE', '')
        title = params.get('TITLE', '')
        sound = params.get('SOUND', '')
        priority = params.get('PRIORITY', 0)
        retry = params.get('RETRY', 30)
        expire = params.get('EXPIRE', 90)

        # Help Message
        if message == '':
            self.gcode.respond_info(HELP)
            return

        # send message
        data = {
            'token': self.api_key,
            'user': self.user_key,
            'device': device_id,
            'title': title,
            'sound': sound,
            'message': message,
            'priority': priority,
        }
        if priority == 2:
            data.update({
                'retry': retry,
                'expire': expire,
            })
        try:
            self.gcode.respond_info(f'Sending {device_id} message: {title} - {message}')
            r = requests.post('https://api.pushover.net/1/messages.json', data=data)
            resp_message = r.json()
            if r.ok:
                self.gcode.respond_info(f'{r.status_code} {r.reason}: {resp_message}')
            else:
                raise self.gcode.error(f'{r.status_code} {r.reason}: {resp_message}')
        except Exception as e:
            raise self.gcode.error(f'Error: {e}')

def load_config(config):
    return Notify(config)
