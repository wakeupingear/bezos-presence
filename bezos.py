import asyncio
import json
import os
import threading
import signal
import sys
import time
from pypresence import Presence
import re

from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

appIDs = {
    'amazon': ['Amazon Music.exe'],
    'spotify': ['Spotify.exe'],
    'itunes': ['iTunes.exe'],
    'edge': ['msedge.exe'],
    'chrome': ['chrome.exe'],
    'firefox': ['firefox.exe'],
}

# https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python

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
    "remove_feat": True,
    "check_interval": 5,
    "no_parentheses": True,
    "apps": ["amazon"],
    "bezos_mode": False,
    "listening_to": "",
    "artist_first": False,
}
default = {
    "album_title": "",
    "artist": "",
    "title": "",
    "app_name": "",
}
track = dict(default)


async def get_media_info(validApps):
    sessions = await MediaManager.request_async()

    allSessions = sessions.get_sessions()
    appName = ""
    for current_session in allSessions:
        if current_session:
            # print(current_session.source_app_user_model_id)
            valid = ("*" in validApps)
            for app in validApps:
                if (app == "*"):
                    continue
                if current_session.source_app_user_model_id in appIDs[app]:
                    appName = app
                    valid = True
                    break
            if valid:
                try:
                    info = await current_session.try_get_media_properties_async()
                except:
                    # opening the app without music playing sometimes
                    # fills the box with null data, causing a crash
                    return None

                # song_attr[0] != '_' ignores system attributes
                info_dict = {song_attr: info.__getattribute__(
                    song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

                # converts winrt vector to list
                info_dict['genres'] = list(info_dict['genres'])
                info_dict['app_name'] = appName
                return info_dict

    return None


def setup(isDev):
    if os.path.exists('settings.json') and not isDev:
        with open('settings.json', 'r') as f:
            settings.update(json.load(f))
    else:
        with open('settings.json', 'w') as f:
            json.dump(settings, f)


def connect():
    if (settings["bezos_mode"]):
        RPC = Presence(client_id='919485848028872715', pipe=0)
    else:
        RPC = Presence(client_id='917341970790244362', pipe=0)
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
        data = [track['title'], track['artist'], track['album_title']]
        if (data[0] == "" and data[1] == "" and data[2] == ""):
            RPC.clear()
            print("Cleared")
            return

        if (settings['artist_first']):
            data = [track['artist'], track['title'], track['album_title']]

        # Parse current track
        if (data[0] == data[1]):  # If artist and title are the same, remove title
            data[1] = ""
        elif (data[0] == ""):  # Artist is empty
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
                if (data[i].find("feat") != -1):
                    data[i] = data[i][:data[i].find("feat")].strip()
        if (settings["no_parentheses"]):
            for i, val in enumerate(data):
                data[i] = re.sub(r"\([^()]*\)", "", val).strip()

        header = settings["listening_to"]+data[0]
        details = data[1]
        if (data[2] != ""):
            if (data[1] != ""):
                details += " - " + data[2]
            else:
                details = data[2]

        photoData = ["fakephoto", "joe"]
        if (settings["bezos_mode"]):
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
