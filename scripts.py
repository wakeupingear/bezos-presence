from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

appIDs = {
    'amazon': ['Amazon Music.exe'],
    'spotify': ['Spotify.exe'],
    'itunes': ['iTunes.exe'],
    'edge': ['msedge.exe'],
    'chrome': ['chrome.exe'],
    'firefox': ['firefox.exe'],
}

# https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python


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
                    return

                # song_attr[0] != '_' ignores system attributes
                info_dict = {song_attr: info.__getattribute__(
                    song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

                # converts winrt vector to list
                info_dict['genres'] = list(info_dict['genres'])
                info_dict['app_name'] = appName
                return info_dict

    return None
