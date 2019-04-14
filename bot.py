#This was made in a few hours, so i apologise for conventional errors

import private #Local file

import spotipy
import spotipy.util as util
import praw
import time

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


def addSongsToPlaylist(songs, spotifyObject):
    # If there's no songs to add to the playlist, just break out of the function
    if(len(songs) == 0):
        return
    username = private.username
    playListID = private.playListID
    spotifyObject.user_playlist_add_tracks(username, playListID, songs, position=None)

def fetchSongsFromReddit(spotifyObject):
    songs=[]
    #Log-into reddit
    reddit = praw.Reddit(client_id=private.redditClient,
                         client_secret=private.redditSecret,
                         user_agent=private.redditAgent,
                         username=private.redditUserName,
                         password=private.redditPassword)
    subreddit = reddit.subreddit('edm')
    #Get the newest 5 posts
    posts = subreddit.new(limit=5)
    for submission in posts:
        if(submission.link_flair_text == "New" and "spotify" in submission.url):
            #Deal with a single track
            if("track" in submission.url):
                songs.append(submission.url)
            #Deal with an album (to come)
            elif("album" in submission.url):
                #Deal with an album
                albumURL = submission.url
                albumURI = dealWithAlbums(spotifyObject, albumURL)
                songs = songs + albumURI
    return songs

def dealWithAlbums(spotifyObject, albumURL):
    URIs = []
    #Get dict of tracks in album
    albumTracks = spotifyObject.album_tracks(albumURL)
    #Parse the dict for song URL's
    for i in range(albumTracks['total_tracks']):
        URIs.append(albumTracks['tracks']['items'][i]['uri'])
    return URIs

def checkForDuplicates(songs):
    newSongs = []
    #Pull all songs in the playlist
    uriInPlayList = getURIInPlayList(spotifyObject)
    #If there are duplicates, don't add the to the "new songs" list
    for i in range(len(songs)):
        if (spotifyObject.track(songs[i])["uri"] not in uriInPlayList):
            newSongs.append(spotifyObject.track(songs[i])["uri"])
    return newSongs


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


# Implemented in delete_playlist.py

# def deleteAllSongs(spoyifyObject):
#     # Pull all songs in the playlist
#     songsInPlayList = getURIInPlayList(spotifyObject)
#     spotifyObject.user_playlist_remove_all_occurrences_of_tracks(private.username, private.playListID, songsInPlayList)


#Continuously run
while True:
    spotifyObject = LogIntoSpotify()
    songs = fetchSongsFromReddit(spotifyObject)
    songs = checkForDuplicates(songs)
    addSongsToPlaylist(songs, spotifyObject)
    time.sleep(60)
