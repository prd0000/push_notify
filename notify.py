import http.client, urllib, os, subprocess,json

class Notify:
    def __init__(self, config) -> None:
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        filename = self.printer.lookup_object('print_stats')

        # configuration
        self.api_key = config.get('api_key')
        self.user_key = config.get('user_key')
        self.timeout = config.get('timeout', 10)
        self.filename = filename.filename

        # Register commands
        self.gcode.register_command(
            "PUSH_NOTIFY", 
            self.cmd_PUSH_NOTIFY, 
            desc=self.cmd_PUSH_NOTIFY_help)

    cmd_PUSH_NOTIFY_help = "Sending message to pushover server"
    def cmd_PUSH_NOTIFY(self, params):
        message = params.get('MSG', '')
        device_id = params.get('DEVICE', '')
        title = params.get('TITLE', self.filename)

        # self.gcode.respond_info(message_params)
        # self.gcode.respond_info(device_id)
        # self.gcode.respond_info(title)

        # send message
        self.gcode.respond_info(f"Sending {device_id} message: {title} - {message}");
        conn = http.client.HTTPSConnection("api.pushover.net", 443,timeout = self.timeout)
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": self.api_key,
            "user": self.user_key,
            "device": device_id,
            "title": title,
            "message": message
        }), { "Content-type": "application/x-www-form-urlencoded" })
        response = conn.getresponse()
        message = response.read().decode()
        if response.status == 200:
            self.gcode.respond_info(f"{response.status} {response.reason}: {message}")
        else:
            raise self.gcode.error(f"{response.status} {response.reason}: {message}")

def load_config(config):
    return Notify(config)