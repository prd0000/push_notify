# Klipper extension for Pushover notification
#
# Copyright (C) 2023  Rudy Dajoh <prd0000@gmail.com>
#
# This file may be distributed under the terms of the GNU AGPLv3 license.

import http.client, urllib

class FCM:
    def __init__(self, config) -> None:
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        filename = self.printer.lookup_object('print_stats')

        # configuration
        self.topic = config.get('topic', "printer")
        self.timeout = config.get('timeout', 10)
        self.server = config.get('server', "ntfy.sh")
        self.serverport = config.get('serverport', "443")

        # Register commands
        self.gcode.register_command(
            "FCM_NOTIFY", 
            self.cmd_FCM_NOTIFY, 
            desc=self.cmd_FCM_NOTIFY_help)
    
    cmd_FCM_NOTIFY_help = "Sending message to FCM server"
    def cmd_FCM_NOTIFY(self, params):
        message = params.get('MSG', '')
        title = params.get('TITLE', '')

        if message == '':
            self.gcode.respond_info('Google FCM based push notification for Klipper.\nUSAGE: FCM_NOTIFY MSG="message" [TITLE="title"]\nTITLE parameter is optional')
            return

        # send message
        self.gcode.respond_info(f"Sending FCM message: {title} - {message}");
        try:
            conn = http.client.HTTPSConnection(f"{self.server}", f"{self.serverport}",timeout = self.timeout)
            conn.request("POST", f"/{self.topic}", message, { "Content-type": "application/x-www-form-urlencoded", "Title": title, "Priority": 3 })
            response = conn.getresponse()

            message = response.read().decode()
            if response.status == 200:
                self.gcode.respond_info(f"{response.status} {response.reason}: {message}")
            else:
                raise self.gcode.error(f"{response.status} {response.reason}: {message}")
            

def load_config(config):
    return FCM(config)