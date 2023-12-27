# Push Notification for Klipper</h1>

<p>
  <a><img src="https://img.shields.io/github/license/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/stars/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/forks/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/languages/top/prd0000/push_notify?logo=gnubash&logoColor=white"></a>
  <a><img src="https://img.shields.io/github/v/tag/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/last-commit/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/contributors/prd0000/push_notify"></a>
</p>


## Introduction

I have been wanting to make my printer notify me whenever it finishes any print for some time now. And after I heard about Klipper, I soon realize that it can use python to extend its functionality. So I wrote this script to help me. And I hope this script can help you, too. 

This simple script will add push notification capabilty to Klipper. 

Klipper is a open source 3D Printer firmware. If you want to install Klipper, you can go to [Klipper 3D](https://www.klipper3d.org/) for detailed instruction

## What you need


This script is using either [Pushover](https://pushover.net/) or the free [ntfy.sh](https://ntfy.sh/) to send push notification to your phone. 

* Pushover service is more secure, but it is a paid service. To utilize Pushover, you will need an account at Pushover to start. Please follow the link for registration detail. After you have registered, you'll receive your ***User key***. Then you have to create your ***API key*** for this script. 

* ntfy.sh is a free service, and you can create any topic you like. Make sure the topic is unique enough to not receive other people's push notification. The topic is essentially your "password". I don't use private ntfy server because I don't deem a 3D printer notification such as out of filament or printing status to be something sensitive. To utilize ntfy.sh, you only need to pick up a topic, and match it to your phone and ***Topic*** entry at configuration file.

## Installation

<ol><li>

Download the source code of [notify.py](https://raw.githubusercontent.com/prd0000/push_notify/main/script/notify.py) if you want to use Pushover, or [fcm.py](https://raw.githubusercontent.com/prd0000/push_notify/main/script/fcm.py) if you want to use ntfy.sh.

<li> 

Copy the script into `<klipper folder>/klippy/extras` folder. 

![Alt text](resources/image.png)

<li> 

Add one of these to your `printer.cfg` configuration
```
[notify]
api_key: <your api key>
user_key: <your user key>
```

or
```
[fcm]
topic: <your topic>
server: <your ntfy hostname, requires tls #OPTIONAL defaults to NTFY.SH>
serverport: <your ntfy server port, requires tls #OPTIONAL defaults to 443>
```

<li>

After you add the section to printer.cfg, do `FIRMWARE_RESTART` at Klipper. 
</ol>

## Usage

<ul><li>

### Syntax
You can put it in any G-Code file like:

```
PUSH_NOTIFY MSG=<message> [DEVICE=<device>] [TITLE=<title>] [SOUND=<sound>]
```

```
FCM_NOTIFY MSG=<message> [TITLE=<title>]
```


* `MSG`: (mandatory) is the message that you are going to send to your phone.

* `DEVICE`: (optional) send a device id. This is corresponds to your device id registered at Pushoverr.

* `TITLE`: (optional) put a title to the message. If you omit this, the script will default to empty string

* `SOUND`: (optional) use a specific sound for the notification (Credits to [@Xierion](https://github.com/Xierion))


<li>

### Command example:

```
PUSH_NOTIFY DEVICE="my_phone" TITLE="filename.gcode" MSG="printing done"
```
```
FCM_NOTIFY TITLE="filename.gcode" MSG="printing done"
```
<li>

### Macro example

Or you can also put it in your macro like:

```
[gcode_macro END_PRINT]
gcode:

    # Turn off bed, extruder, and fan
    M140 S0
    M104 S0
    M106 S0
    # Move nozzle away from print while retracting
    G91
    G1 Z10 E-5 F300
    G90
    G1 X10 Y300 F3000
    # Disable steppers
    M84
    # Notify User
    PUSH_NOTIFY MSG="Printing Done"

```

</ul>

Enjoy