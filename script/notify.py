# Klipper extension for ntfy notification
#
# Copyright (C) 2023  Rudy Dajoh <prd0000@gmail.com>
#
# This file may be distributed under the terms of the GNU AGPLv3 license.
import threading
import http.client, urllib

class Notify:    
    def __init__(self, config):
        # self.name = config.get_name().split()[-1]
        # self.printer = config.get_printer()
        # self.gcode = self.printer.lookup_object('gcode')
        # filename = self.printer.lookup_object('print_stats')

        # configuration
        self.url = config.get('url', "")
        self.timeout = config.get('timeout', 10)
        self.headers = config.get('headers', '')
        self.body = config.get('body', "")
        self.method = config.get('method', "POST").upper()

        # Register commands
        self.gcode.register_command(
            "NOTIFY", 
            self.cmd_NOTIFY, 
            desc=self.cmd_NOTIFY_help)


    def send_notification(self, title, message):
        try:
            body = self.body.replace('{MSG}', message).replace('{TITLE}', title)
            headers = {
                k: v.replace('{MSG}', message).replace('{TITLE}', title)
                for k, v in self.headers.items()
            }
            
            response = response.request(
                method=self.method, 
                url=self.url,
                body=body, 
                headers=headers
            )   

            # body = response.read().decode()
            if response.status == 200:
                self.gcode.respond_info(f"{response.status} {response.reason}: {body}")
            else:
                raise self.gcode.error(f"{response.status} {response.reason}: {body}")
                
            conn.close()
                
        except Exception as e:
            raise self.gcode.error(f"Error: {e}")

    def fcm(self, config):

    cmd_NOTIFY_help = "Sending message to push notification server"
    def cmd_NOTIFY(self, params):
        message = params.get('MSG', '')
        title = params.get('TITLE', '')

        if self.url == '':
            self.gcode.respond_info('Push notification module for Klipper.\nPlease set the URL parameter in the configuration file.')
            return

        if message == '':
            self.gcode.respond_info('Push notification module for Klipper.\nUSAGE: NOTIFY MSG="message" [TITLE="title"]\nTITLE parameter is optional')
            return

        # send message
        self.gcode.respond_info(f"Sending {self.url}: {title} - {message}")
        self.gcode.respond_info(f"Method: {self.method}")
        self.gcode.respond_info(f"Headers: {self.headers}")
        self.gcode.respond_info(f"Body: {self.body}")   
        


def load_config(config):
    return Notify(config)
