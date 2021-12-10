from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

appIDs = {
    'amazon': ['Amazon Music.exe'],
    'spotify': ['Spotify.exe']
}

# https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python


async def get_media_info(validApps):
    sessions = await MediaManager.request_async()

    allSessions = sessions.get_sessions()
    for current_session in allSessions:
        if current_session:
            valid = ("*" in validApps)
            if not valid:
                for app in validApps:
                    if current_session.source_app_user_model_id in appIDs[app]:
                        valid = True
                        break
            if valid:
                info = await current_session.try_get_media_properties_async()

                # song_attr[0] != '_' ignores system attributes
                info_dict = {song_attr: info.__getattribute__(
                    song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

                # converts winrt vector to list
                info_dict['genres'] = list(info_dict['genres'])
                return info_dict

    return None
