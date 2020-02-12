#===============================================================================
# SCRAPE SPOTIFY USER PLAYLISTS
#===============================================================================
#   INPUTS:
#       * user URI
#       * key phrase (if key in playlist name, playlist will be scraped)
#   OUTPUTS (written into CSV file):
#       * song names (of songs in playlists containing key)
#       * song URIs (of songs in playlists containing key)
#===============================================================================
# 1.CHOOSE INPUTS AND OUTPUTS

# CHOOSE USER (comment/uncomment relevant user)
user = "stealthamo"
# user = "wormwood37"

# KEY PHRASE IN PLAYLIST NAME (comment/uncomment relevant key)
key = "Billboard Year End Hot 100"
# key = "The Billboard Hot 100 Complete History of Pop"

# CHOOSE CSV FILE TO WRITE INTO
fileName = "spotifyData_100perYr_final.csv"
# fileName = "spotifyData_billboardDecadeData_final.csv"

# ***code below must be altered depending on user
#===============================================================================
# 2.SET UP (ignore this section)

# IMPORT MODULES
import spotipy
import numpy as np
import pandas as pd
import os
import csv
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

# IF OUTPUT CSV FILE DOESN'T EXIST OR IS EMPTY, WRITE COLUMN NAMES INTO FILE
if not(os.path.exists(fileName)) or os.stat(fileName).st_size == 0:
    with open(fileName, 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(["date","songName","songURI","artistName","artistURI",
                         "albumName","albumURI","acousticness","danceability",
                         "energy","instrumentalness","liveness","loudness",
                         "speechiness","tempo","valence","duration_ms",
                         "mode","key","time_signature","popularity"])

# SET UP SPOTIPY
client_id = "6f01fd29f27d4ab5b96aa24aa35df389"
client_secret = "485a8bcab1be4e92977ef2bf023b88eb"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

#===============================================================================
# 3.RETRIEVE PLAYLIST DATA (year, playlist name, playlist uri)

# CREATE EMPTY LISTS FOR PLAYLIST DATA
playlistYear = []
playlistNames = []
playlistURIs = []

# FUNCTION TO GET ALL PLAYLISTS FROM A USER
def get_playlist(username):
    results = sp.user_playlists(username)
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    return playlists

# SEARCH USER FOR PLAYLISTS
playlists = get_playlist(user)

# FOR EVERY PLAYLIST:
for i in range(len(playlists)):
    # IF KEY PHRASE IS IN PLAYLIST NAME:
    if key in playlists[i]['name']:
        # ***depending on user comment/uncomment relevant section
        #=======================================================================
        # ***UNCOMMENT THIS SECTION IF SCRAPING USER "stealthamo"

        # FIND THE YEAR IN PLAYLIST NAME
        year = int(playlists[i]['name'][:4]) # year = first 4 strings in playlist name

        # TAKE ONLY PLAYLISTS OF BILLBOARD DATA AFTER 1980
        if year >= 1980:
            # APPEND YEAR, PLAYLIST NAME, PLAYLIST URI TO RELEVANT LISTS
            playlistYear.append(year)
            playlistNames.append(playlists[i]['name'])
            playlistURIs.append(playlists[i]['uri'])

        #=======================================================================
        # # ***UNCOMMENT THIS SECTION IF SCRAPING USER "wormwood37"
        #
        # # FIND THE YEAR IN PLAYLIST NAME
        # year = playlists[i]['name'].split(": ")[0] # year = string before ": "
        #
        # # APPEND YEAR, PLAYLIST NAME, PLAYLIST URI TO RELEVANT LISTS
        # playlistYear.append(year)
        # playlistNames.append(playlists[i]['name'])
        # playlistURIs.append(playlists[i]['uri'])
        #=======================================================================

#===============================================================================
# 4.RETRIEVE SONG URIs AND CHART YEAR FOR EVERY SONG IN EVERY PLAYLIST

# FUNCTION TO GET ALL TRACKS IN A PLAYLIST
def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

songYear = []
songURIs = []

# FOR EVERY PLAYLIST:
for j in range(len(playlistURIs)):
    # GET TRACKS IN PLAYLIST
    uri = playlistURIs[j]
    songs = get_playlist_tracks(user, uri)

    # FOR EVERY TRACK:
    for k in range(len(songs)):
        # APPEND YEAR, SONG NAME, SONG URI TO LISTS
        songYear.append(playlistYear[j])
        songURIs.append(songs[k]['track']['uri']])

#===============================================================================
# 5.RETRIEVE SPOTIFY AUDIO FEATURES FOR SONGS

# FOR ALL SONGS IN BILLBOARD DATA:
for k in range(len(songURIs)):
    # GET SONG URI
    songURI = songURIs[k]

    # PULL SPOTIFY DATA ABOUT CHOSEN SONG
    songData = sp.track(songURI)

    # INCASE THERE ARE MULTIPLE ARTISTS, ADD THEM TOGETHER INTO ONE STRING
    artistsNames = songData['artists'][0]['name']
    artistsURIs = songData['artists'][0]['uri']
    if len(songData['artists'])>1:
        for j in range(len(songData['artists'])-1):
            artistsNames += (";"+songData['artists'][j+1]['name'])
            artistsURIs += (","+songData['artists'][j+1]['uri'])

    # PULL SPOTIFY FEATURES ABOUT CHOSEN SONG
    features = sp.audio_features(songURI)

    # SAVE NECESSARY DATA INTO A ROW
    row = [
        songYear[k],
        songData['name'],
        songURI,
        artistsNames,
        artistsURIs,
        songData['album']['name'],
        songData['album']['uri'],
        features[0]['acousticness'],
        features[0]['danceability'],
        features[0]['energy'],
        features[0]['instrumentalness'],
        features[0]['liveness'],
        features[0]['loudness'],
        features[0]['speechiness'],
        features[0]['tempo'],
        features[0]['valence'],
        features[0]['duration_ms'],
        features[0]['mode'],
        features[0]['key'],
        features[0]['time_signature'],
        songData['popularity']
        ]
    # APPEND ROW TO CSV FILE
    with open(fileName, 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(row)

    # SAVE INDEX OF LAST APPENDED ROW
    allDataIndex = i    # incase program stops restart scraping from this index
