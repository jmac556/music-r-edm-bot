#This was written in 3 hours

import private #Local file

import spotipy
import spotipy.util as util
import praw

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
    #If there's no songs to add to the playlist, just break out of the function
    if(len(songs) == 0):
        return
    username = private.username
    playListID = private.playListID
    spotifyObject.user_playlist_add_tracks(username, playListID, songs, position=None)

def fetchSongsFromReddit():
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
            if("album" in submission.url):
                #Deal with an album
                print("Album............", submission.title)
    return songs


def checkForDuplicates(songs):
    newSongs = []
    #Pull all songs in the playlist
    songsInPlayList = spotifyObject.user_playlist_tracks(private.username, playlist_id=private.playListID, limit=100)
    uriInPlayList = []
    #Parse out the uri from the playlist attributes
    for item in songsInPlayList['items']:
        if 'track' in item:
            track = item['track']
        else:
            track = item
        try:
            track_uri = track['uri']
            uriInPlayList.append(track_uri)
    #LINES UNTIL 73 UNNECCESSARY!!!
        except KeyError:
            print("Except: Line 69")
            # 1 page = 50 results
            # check if there are more pages
    # if tracks['next']:
    #     tracks = spotify.next(tracks)
    # else:
    #     break

    #If there are duplicates, don't add the to the "new songs" list
    for i in range(len(songs)):
        if (spotifyObject.track(songs[i])["uri"] not in uriInPlayList):
            newSongs.append(spotifyObject.track(songs[i])["uri"])
    return newSongs


spotifyObject = LogIntoSpotify()
songs = fetchSongsFromReddit()
songs = checkForDuplicates(songs)
addSongsToPlaylist(songs, spotifyObject)
