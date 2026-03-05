# Template for notification services.
# 
# Copyright (C) 2026  Rudy Dajoh
# This file may be distributed under the terms of the GNU AGPLv3 license.
#
#
# This is a template for creating notification services. You can use this as a starting point for your own notification service.
# All variables are marked with {}. Lowercase {variables} are replaced with configuration, 
# while uppercase {VARIABLES} are replaced with GCODE.
# Text inside square brackets [] is optional and will only be included if the variables inside are provided.
#
# Body is a string.
#

TEMPLATES = {
    'ntfy': {
        "url": 'https://ntfy.sh/{topic}',
        "headers": """
            Content-Type:application/x-www-form-urlencoded
            Priority:3
            [Title:{TITLE}]
        """,
        'body': '{MSG}',
        'method': 'POST'
    }, 
    "pushover": {
        'url': 'https://api.pushover.net/1/messages.json',
        'headers': """
            Content-Type:application/x-www-form-urlencoded
        """,
        'body': 'topic={topic}&token={token}&user={user}&device={device}&title={title}&sound={sound}&message={MSG}&priority={priority}[&retry={retry}][&expire={expire}]',
        'method': 'POST'
    },
    "pushbullet": {
        "url": "https://api.pushbullet.com/v2/pushes",
        "method": "POST",
        "timeout": 10,
        "headers":
        """
            Access-Token: {token}
            Content-Type: application/json
        """,
        "body":
            {"body":"{MSG}"[,"title":"{TITLE}"],"type":"note"}',
    }
}
