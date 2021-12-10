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

settings = {
    "remove_explicit": True,
    "remove_clean": True,
    "remove_feat": False,
    "check_interval": 5,
    "no_parentheses": True,
    "apps": ["amazon"]
}
track = {
    "album_title": "",
    "artist": "",
    "title": "",
}

client_id = '917341970790244362'


def setup():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            settings.update(json.load(f))
    else:
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    client_id = '917341970790244362'


def connect():
    RPC = Presence(client_id, pipe=0)
    RPC.connect()
    return RPC


def checkMusic(RPC):
    threading.Timer(settings['check_interval'], checkMusic, [RPC]).start()
    media = asyncio.run(get_media_info(settings["apps"]))
    if (media == None):
        RPC.clear()
        return
    media = {k: v for k,
             v in media.items() if k in track}
    if (media != track):
        track.update(media)
        temp = dict(track)

        # Parse current track
        if (temp["artist"] == temp["title"]):
            temp["artist"] = ""
            temp["title"] = "Listening to " + temp["title"]
        else:
            if (temp["artist"] != ""):
                temp["artist"] = "by " + temp["artist"]
            else:
                temp["title"] = "Listening to '" + temp["title"] + "'"
        # Apply settings
        if (settings["remove_explicit"]):
            temp["title"] = temp["title"].replace("[Explicit]", "").strip()
            temp["artist"] = temp["artist"].replace("[Explicit]", "").strip()
        if (settings["remove_clean"]):
            temp["title"] = temp["title"].replace("[Clean]", "").strip()
            temp["artist"] = temp["artist"].replace("[Clean]", "").strip()
        if (settings["remove_feat"]):
            temp["title"] = re.sub(r"\[[^()]*\]", "", temp["title"]).strip()
            temp["artist"] = re.sub(r"\[[^()]*\]", "", temp["artist"]).strip()
        if (settings["no_parentheses"]):
            temp["title"] = re.sub(r"\([^()]*\)", "", temp["title"]).strip()
            temp["artist"] = re.sub(r"\([^()]*\)", "", temp["artist"]).strip()

        header = temp["title"]
        if (header != "" and header[0] != "'"):
            header = "'" + header + "'"
        details = temp["artist"]
        if (details == "" and header == ""):
            RPC.clear()
            return
        elif (header == ""):
            RPC.update(state=details)
        elif (details == ""):
            RPC.update(state=header)
        else:
            RPC.update(state=details, details=header)
        print(temp)


def main():
    setup()

    isDev = False
    for i, arg in enumerate(sys.argv):
        if (arg == '--dev'):
            isDev = True
            print("Running in dev mode")

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
