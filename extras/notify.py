# Klipper extension for ntfy notification
#
# Copyright (C) 2023  Rudy Dajoh <prd0000@gmail.com>
#
# This file may be distributed under the terms of the GNU AGPLv3 license.
# 

import re, json, threading, http.client
from urllib.parse import urlparse
from .server_template import TEMPLATES

class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class Notify:    
    def __init__(self, config):
        
        # Initialize the extension
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.reactor = self.printer.get_reactor()
        filename = self.printer.lookup_object('print_stats')

        # Loading configuration
        self.config = {}
        self.parameters = set()
        self.timeout = config.get('timeout', 10)
        template_name = config.get('template', False)
        if template_name:
            self.template = TEMPLATES.get(template_name, False)
            if not self.template:
                raise Exception(f"Template '{template_name}' not found.")
        else:
            self.template = {
                "url": config.get('url'),
                "headers": config.get('headers', ''),
                "body": config.get('body', ''),
                "method": config.get('method', 'POST').upper(),
                "usage": config.get('usage', '')
            }
            
        #extract configuration variables
        template = "\n".join(str(v) for v in self.template.values())
        vars = set(re.findall(r'\{([a-zA-Z_]\w*)\}', template))
        for k in vars:
            if k.isupper():
                self.parameters.add(k)              # UPPERCASE, save for GCODE template
            else:
                self.config[k] = config.get(k, '')  # Others, get from configuration

        # Register commands
        self.gcode.register_command(
            "NOTIFY", 
            self.cmd_NOTIFY, 
            desc="Universal message notifier")

    def validate(self, params):
        if not self.template.get('url'):
            raise Exception('PUSH NOTIFY: Please configure the extension.')

    def _safe_respond(self, message):
        self.reactor.register_callback(lambda e: self.gcode.respond_info(message))
        return None

    def process(self, param):
        def replace_placeholders(template, values):

            def replace_block(match):
                key = match.group(1)
                try:
                    return key.format_map(values)
                except KeyError:
                    return ""

            optional_template = re.sub(r'\[(.*?)\]', replace_block, template)
            return optional_template.format_map(SafeDict(values))
        
        def send_notification(req_data):
            # Parse URL into components
            url = urlparse(req_data["url"])
            
            # Create connection
            ConnectionClass = http.client.HTTPSConnection if url.scheme == "https" else http.client.HTTPConnection
            conn = ConnectionClass(url.netloc, timeout=self.timeout)
            
            try:
                # Execute request
                conn.request(
                    method=req_data["method"],
                    url=url.path or "/", 
                    body=req_data["body"],
                    headers=req_data["headers"]
                )
                
                # Get and read response
                response = conn.getresponse()
                body = response.read().decode()
                result = {
                    "status": response.status,
                    "reason": response.reason,
                    "body": body
                }
            except Exception as e:
                result = {
                    "status": False,
                    "reason": e
                }
            finally:
                conn.close()
                return result

        # Gather all parameters
        parameters = self.config
        for k in self.parameters:
            p = param.get(k, False)
            if p:
                parameters[k] = p

        # Generate Payload
        payload = {
            k: replace_placeholders(self.template.get(k), parameters)
            for k in {'url', 'method', 'body'}
        }

        # generate Header
        raw_header = replace_placeholders(self.template.get('headers'), parameters)
        header_dict = {}
        for line in raw_header.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                header_dict[key.strip()] = value.strip()
        payload['headers'] = header_dict
        
        return send_notification(payload)

    def cmd_NOTIFY(self, parameters):
        def wrapper():
            try:
                result = self.process(parameters)
                if not result.get('status'):
                    error = result.get('reason')
                    self._safe_respond("ERROR: {error}")
                else:
                    body = result.get('body')
                    self._safe_respond(body)

            except Exception as e:
                self._safe_respond(body)

        # Help asked
        if parameters.get('HELP', False):
             self.gcode.respond_info('Universal message notifier for Klipper.\nUSAGE: NOTIFY ' + self.usage + '\nHELP parameter is optional')
             return

        try:
            self.validate(parameters)
            thread = threading.Thread(target=wrapper)
            thread.start()
            self._safe_respond("Sending notification")
        except Exception as e:
            self._safe_respond(f"Error: {e}")

def load_config(config):
    return Notify(config)