# Bezos Presence - actual useful settings
Bezos Presence can be configured by editing the values in `settings.json`
## Disable Bezos Mode
First things first, if you actually want to use this as a real media plugin, you need to set the `bezos_mode` flag to `false`. This will change the status to "Playing Music" and allow the default photo to be overridden.

## Settings
`remove_explicit`: Remove explicit tags from song and album titles

`remove_clean`: Remove clean tags

`remove_feat`: Remove featured artists (these usually overflow off the Discord window)

`check_interval`: How often the program checks for music changes (in seconds)

`no_parentheses`: Removes parentheses

`validApps`: A list of every app that can trigger the plugin. Each entry needs to match the App ID (see the `apps` category below). Entering a `*` will allow any app in the `apps` category to work.

`listening_to`: Appends text in front of the currently playing media. For example, this could be set to 'Listening to '.

`artist_first`: Whether the artist should come first or second.

`photo_override`: Override the default image that appears. This only works for valid Image IDs that I've already uploaded to the Discord admin panel, so linking your own images or URLs **will not work**.

`apps`: A collection of all possible apps. For an app that plays audio to be recognized, it needs to have an entry in this list. The key is the App ID, and the entries in the list for each mean the following:
<ol>
    <li>The corresponding image ID for this app. These images need to be stored on the Discord admin end, so only the default apps work. Leave this blank for additional apps.</li>
    <li>The app name.</li>
    <li>A list of all applications that are counted as this app. These NEED to match the exact executable name for each of these apps. For example, Microsoft Edge is actually msedge.exe.</li>
</ol>