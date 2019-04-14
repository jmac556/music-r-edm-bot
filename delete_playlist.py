#To run by crontab every Wednesday night

import private #Local file

import spotipy
import spotipy.util as util

def LogIntoSpotify():
    # Credentials held in a separate file called 'private'

    # Get authorization from Spotify
    token = util.prompt_for_user_token(private.username,
                                       'playlist-modify',
                                       client_id=private.clientId,
                                       client_secret=private.clientSecret,
                                       redirect_uri=private.redirectURI)
    # Create spotify object
    return spotipy.Spotify(auth=token)

def getURIInPlayList(spotifyObject):
    #Pull all info about the playlist
    songsInPlayList = spotifyObject.user_playlist_tracks(private.username, playlist_id=private.playListID, limit=100)
    uriInPlayList = []
    # Parse out the uri from the playlist attributes
    for item in songsInPlayList['items']:
        if 'track' in item:
            track = item['track']
        else:
            track = item
        try:
            track_uri = track['uri']
            uriInPlayList.append(track_uri)
            # LINES UNTIL 73 UNNECCESSARY!!!
        except KeyError:
            print("Except: Line 112")
    return uriInPlayList


def deleteAllSongs(spotifyObject):
    # Pull all songs in the playlist
    songsInPlayList = getURIInPlayList(spotifyObject)
    spotifyObject.user_playlist_remove_all_occurrences_of_tracks(private.username, private.playListID, songsInPlayList)


spotify = LogIntoSpotify()
deleteAllSongs(spotify)