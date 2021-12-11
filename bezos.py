import asyncio
import json
import os
import threading
import signal
import sys
import time
from pypresence import Presence
import re

from scripts import *

appData = {
    "amazon": ["amazon", "Amazon Music"],
    "spotify": ["spotify", "Spotify"],
    "itunes": ["itunes", "iTunes"],
    "edge": ["edge", "Microsoft Edge"],
    "chrome": ["chrome", "Google Chrome"],
    "firefox": ["firefox", "Firefox"],
}
settings = {
    "remove_explicit": True,
    "remove_clean": True,
    "remove_feat": False,
    "check_interval": 5,
    "no_parentheses": True,
    "apps": ["amazon"],
    "funny_photo": True
}
default = {
    "album_title": "",
    "artist": "",
    "title": "",
}
track = dict(default)

client_id = '917341970790244362'


def setup(isDev):
    if os.path.exists('settings.json') and not isDev:
        with open('settings.json', 'r') as f:
            settings.update(json.load(f))
    else:
        with open('settings.json', 'w') as f:
            json.dump(settings, f)


def connect():
    RPC = Presence(client_id, pipe=0)
    RPC.connect()
    return RPC


def checkMusic(RPC):
    threading.Timer(settings['check_interval'], checkMusic, [RPC]).start()
    media = asyncio.run(get_media_info(settings["apps"]))
    if (media == None):
        media = dict(default)
    appName = media['app_name']
    media = {k: v for k,
             v in media.items() if k in track}
    if (media != track):
        track.update(media)
        data = [track['artist'], track['title'], track['album_title']]
        if (data[0] == "" and data[1] == "" and data[2] == ""):
            RPC.clear()
            print("Cleared")
            return

        # Parse current track
        if (data[0] == data[1]): # If artist and title are the same, remove title
            data[1] = ""
        elif (data[0] == ""): # Artist is empty
            data[0] = data[1]
            data[1] = ""

        # Apply settings
        if (settings["remove_explicit"]):
            for i, val in enumerate(data):
                data[i] = val.replace("[Explicit]", "").strip()
        if (settings["remove_clean"]):
            for i, val in enumerate(data):
                data[i] = val.replace("[Clean]", "").strip()
        if (settings["remove_feat"]):
            for i, val in enumerate(data):
                data[i] = re.sub(r"\[[^()]*\]", "", val).strip()
        if (settings["no_parentheses"]):
            for i, val in enumerate(data):
                data[i] = re.sub(r"\([^()]*\)", "", val).strip()

        header = "Listening to "+data[0]
        details = data[1]
        if (data[2] != ""):
            if (data[1] != ""):
                details += " - " + data[2]
            else:
                details = data[2]

        photoData = ["fakephoto", "joe"]
        if (settings["funny_photo"]):
            photoData = ["jeffrey", "Jeffrey Music"]
        elif (appName != ""):
            photoData = appData[appName]

        if (details == ""):
            RPC.update(
                state=header, large_image=photoData[0], large_text=photoData[1])
        else:
            RPC.update(state=details, details=header,
                       large_image=photoData[0], large_text=photoData[1])
        print(data)


def main():
    isDev = False
    for i, arg in enumerate(sys.argv):
        if (arg == '--dev'):
            isDev = True
            print("Running in dev mode")
    setup(isDev)

    checkMusic(connect())

    # ctrl+c handler
    def signal_handler(sig, frame):
        os._exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    if isDev:
        while True:
            time.sleep(0.1)


if __name__ == '__main__':
    main()
