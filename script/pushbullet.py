# Klipper extension for Pushbullet notification
#
# Copyright (C) 2023  Rudy Dajoh <prd0000@gmail.com>
#
# This file may be distributed under the terms of the GNU AGPLv3 license.

import sys
sys.path.append("/usr/lib/python3/dist-packages")
import requests
from requests.structures import CaseInsensitiveDict

class Pushbullet:
    def __init__(self, config) -> None:
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')

        # configuration
        self.pb_access_token = config.get('pb_access_token')
        self.timeout = config.get('timeout', 10)

        # Register commands
        self.gcode.register_command(
            "PUSHBULLET_NOTIFY", 
            self.cmd_PUSHBULLET_NOTIFY, 
            desc=self.cmd_PUSHBULLET_NOTIFY_help)

    cmd_PUSHBULLET_NOTIFY_help = "Sending message to Pushbullet server"
    def cmd_PUSHBULLET_NOTIFY(self, params):
        message = params.get('MSG', '')
        title = params.get('TITLE', '')

        # Help Message
        if message == '':
            self.gcode.respond_info('Klipper Push Notification module for Pushbullet.\nUSAGE: PUSHBULLET_NOTIFY MSG="message" TITLE="title"')
            return

        # write to console that we're about to send message
        self.gcode.respond_info(f"Sending message: {title} - {message}");

        # now send the message using pushbullet
        headers = CaseInsensitiveDict()
        headers["Access-Token"] = self.pb_access_token
        headers["Content-Type"] = "application/json"
        data = '{"body":"' + message + '","title":"' + title + '","type":"note"}'
        url = "https://api.pushbullet.com/v2/pushes"
        response = requests.post(url, headers=headers, data=data)

        # return response
        if response.status_code == 200:
            self.gcode.respond_info(f"{response.status_code} {response.reason}")
        else:
            raise self.gcode.error(f"{response.status_code} {response.reason}")

def load_config(config):
    return Pushbullet(config)
