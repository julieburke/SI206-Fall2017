##Name:Julie Burke

## SI 206 2017
## Project 3
import unittest
import json
import sqlite3
import spotipy 
import spotipy.util as util 
from spotipy.oauth2 import SpotifyClientCredentials

import github

def getFacebookData():
	pass

def getInstagramData():
	pass

def getYoutubeData():
	pass

def getMoreData():
	pass

def getGoogleMapsData():
	pass

def getSpotifyData():
	username = 'https://open.spotify.com/user/1227688480'
	scope = 'user-library-read'
	token = util.prompt_for_user_token(username, scope)
	client_credentials_manager = SpotifyClientCredentials()
	sp = spotipy.Spotify(auth=token, client_credentials_manager=client_credentials_manager)

	sp.trace = True # turn on tracing
	sp.trace_out = True # turn on trace out
	user = sp.user(username)
	#token = util.prompt_for_user_token(username, scope)
	
	print (user.current_user_recently_played())

	#results = spotify.
	#GET https://api.spotify.com/v1/me/player/recently-played

#getSpotifyData()
def getAppleHealthData():
	pass
	#https://developer.apple.com/documentation/healthkit

def getGitHubData():
	#git = PyGithub('61dba3f8bc30ed30edb03edab2cf6c40052a0f93')
	g = github.Github('61dba3f8bc30ed30edb03edab2cf6c40052a0f93')
	print (g.get_user())

	#g = Github("julieburke", "Julieblue15!")
	#print (g)
	#print (dir(g))
	#print (g.get_user())
getGitHubData()

def getCanvasData():
	pass

def getGmailData():
	pass