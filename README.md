<p align="center">
  <a>
    <h1 align="center">Push Notification for Klipper</h1>
  </a>
</p>

<p align="center">
  <a><img src="https://img.shields.io/github/license/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/stars/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/forks/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/languages/top/prd0000/push_notify?logo=gnubash&logoColor=white"></a>
  <a><img src="https://img.shields.io/github/v/tag/prd0000/push_notify"></a>
  <br />
  <a><img src="https://img.shields.io/github/last-commit/prd0000/push_notify"></a>
  <a><img src="https://img.shields.io/github/contributors/prd0000/push_notify"></a>
</p>

<hr>

<h2 align="center">
  Introduction
</h2>

This simple script will add push notification capabilty to Klipper. 

Klipper is a open source 3D Printer firmware. If you want to install Klipper, you can go to [Klipper 3D](https://www.klipper3d.org/) for detailed instruction

<h2 align="center"> 
    What you need
</h2>

This script is using [Pushover](https://pushover.net/) to send push notification to your phone. So you will need an account at Pushover to start. Please follow the link for registration detail. 

After you have registered, you'll receive your ***User key***. Then you have to create your ***API key*** for this script. 

<h2 align="center">
    Installation
</h2>

1. Download the source code of [notify.py](https://raw.githubusercontent.com/prd0000/push_notify/main/script/notify.py)

2. Copy the script into `<klipper folder>/klippy/extras` folder

![Alt text](resources/image.png)

3. add this to your printer.cfg configuration
```
[notify]
api_key: <your api key>
user_key: <your user key>
```

After you add the section, do `FIRMWARE_RESTART` at Klipper. 

<h2 align="center">
    Usage
</h2>

You can put it in any G-Code file like:

`PUSH_NOTIFY DEVICE=<device> TITLE=<title> MSG=<message>`

