##Name:Julie Burke

## SI 206 2017
## Project 3
import unittest
import requests
import facebook  #pip install facebook-sdk
import json
import sqlite3
import spotipy 
import spotipy.util as util 
from spotipy.oauth2 import SpotifyClientCredentials
#import gdata
#import gdata.youtube.service
from instagram.client import InstagramAPI

import github

#from InstagramAPI import InstagramAPI


def getFacebookData():
	access_token = 'EAACEdEose0cBAGyhJVCK7vZBdVldCgSPbBym4ZApoAiyO2c1PMnboUotoPSAZAl7SpmBnnvnL4lw0ZA2VW5hAiqucmG98zEGms3dPOm4Of9Tblay22zePFJoZAntIJj60ZA3v02UGNmtDSQqiLlANO0btgEjirDG668x6fLnSZCnjRRyBZCsc1iy4Ul0RZBI5oy0ynfTncntSaAZDZD'
	graph = facebook.GraphAPI(access_token)
	data = graph.get_connections('me','user_work_history') 
	# profile = graph.get_object('me', fields = 'name,location{location}') #fields is an optional key word argument
	return json.dumps(data)
#print (getFacebookData())
def getInstagramData():
	#from instagram.client import InstagramAPI

	client_id = "b21d1a2d5cec4f5a9c676dccd8aeb57b"
	client_secret = "e8809122b94b40218bfb840e099393fd"
	access_token ='53913195.b21d1a2.12381295c6614aeaae1c15a8baa62e56'
	api = InstagramAPI(access_token = access_token, client_id= client_id,client_secret=client_secret)
	recent = api.user_recent_media(user_id="53913195", count=100)
	print (type(recent))
	print (len(recent))
	print (type(recent[0]))
	print (len(recent[0]))
	print (recent[0][1])
	print (recent[1])
	#for media in recent:
   	#	print (media.caption.text)
	#recent_media, next_ = api.user_recent_media(user_id="userid", count=10)
	#for media in recent_media:
  		#print media.caption.text
getInstagramData()
def getYoutubeData():
	pass

def getMoreData():
	pass

def getGoogleMapsData():
	#look at last time
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
#getGitHubData()

def getCanvasData():
	pass

def getGmailData():
	API_KEY = "AIzaSyDK5Xmn3UcnN7oNQur68eM1pols6RE6pcM"
	