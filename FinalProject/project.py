##Name:Julie Burke

## SI 206 2017
## Project 3
import unittest
import requests
import facebook  #pip install facebook-sdk
import json
import sqlite3
import datetime
import spotipy 
import spotipy.util as util 
from spotipy.oauth2 import SpotifyClientCredentials
import re
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
#import gdata
#import gdata.youtube.service
from instagram.client import InstagramAPI

from github import Github

#from InstagramAPI import InstagramAPI

CACHE_FNAME = "final_project_cache.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r') #open your file to read in data from cache file 
    cache_contents = cache_file.read() #read the cache file
    cache_file.close() #close file
    CACHE_DICTION = json.loads(cache_contents) #load file string into json dictionary
except:
    CACHE_DICTION = {}


def getFacebookData():
	if 'facebook' in CACHE_DICTION:
		print("using cache") #let user know what is happening
		return CACHE_DICTION['facebook'] #return the results from cache 
	else:
		print("fetching") #let user know what is happening
		access_token = 'EAACEdEose0cBAIvRYHxTxYIqL49tSx0sHNZAkvPskd2ZBMEvP6H37pvLa1fvwykWZAXVZBb2FdLnRlSZBFNWiJhdevG9JRLskCOAee1TVVuS0zC7ed4vgzOBNL0YZCLVAkdbZCb0cCwW3ZA11PkL7Do2im5PrE5QknsY2wymCGnGioFvvuhjaPWyQAzWDIYnQfQZD'
		graph = facebook.GraphAPI(access_token)
		all_fields = ['created_time']
		day_count = {}
		#all_fields = ','.join(all_fields)
		#data = graph.get_connections('me','user_work_history') 
		posts = graph.get_connections('me','posts', fields = all_fields, limit = 100) 
		for post in posts['data']:
			date = re.findall('([0-9]*-[0-9]*-[0-9]*)T',post['created_time'])
			change = datetime.datetime.strptime(date[0], '%Y-%m-%d')
			day = change.isoweekday()
			if day == 1:
				day = 'Monday'
			if day == 2:
				day = 'Tuesday'
			if day == 3:
				day = 'Wednesday'
			if day == 4:
				day = 'Thursday'
			if day == 5:
				day = 'Friday'
			if day == 6:
				day = 'Saturday'
			if day == 7:
				day = 'Sunday'

			day_count[day] = day_count.get(day, 0) + 1
		CACHE_DICTION['facebook'] =  day_count #put in cache dictionary 
		fw = open(CACHE_FNAME,"w") #open file
		fw.write(json.dumps(CACHE_DICTION)) #write results into cache file 
		fw.close()
		return day_count
	# profile = graph.get_object('me', fields = 'name,location{location}') #fields is an optional key word argument
	#return json.dumps(data)
#getFacebookData()
def getInstagramData():
	#from instagram.client import InstagramAPI

	client_id = "b21d1a2d5cec4f5a9c676dccd8aeb57b"
	client_secret = "e8809122b94b40218bfb840e099393fd"
	access_token ='53913195.b21d1a2.12381295c6614aeaae1c15a8baa62e56'
	api = InstagramAPI(access_token = access_token, client_id= client_id,client_secret=client_secret)
	recent = api.user_liked_media(user_id="53913195", count=100, scope = 'public_content')
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
#getInstagramData()
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


def getGitHubData():
	#git = PyGithub('61dba3f8bc30ed30edb03edab2cf6c40052a0f93')
	#g = github.Github('61dba3f8bc30ed30edb03edab2cf6c40052a0f93')
	#print (g.get_user())

	g = Github("julieburke", "Julieblue15!")
	print ((g.get_repos()._PaginatedList__headers))
	#print (g)
	#print (dir(g))
	#print (g.get_user())
getGitHubData()

def getCanvasData():
	pass

def getGmailData():
	API_KEY = "AIzaSyDK5Xmn3UcnN7oNQur68eM1pols6RE6pcM"

def visualizeDayofWeekData(dictionary):
	plotly.tools.set_credentials_file(username='julieburke', api_key='EnRYcjJL5LUMtyi8Zt5Q')
	days = []
	counts = []
	items = dictionary.items()
	for k,v in items:
		days.append(k)
		counts.append(v)
	print (days)
	print (counts)
	layout = go.Layout(title='Facebook Usage By Day')
	data = [go.Bar(x = days,y = counts)]
	py.iplot(data, file_id='basic-bar')
	#fig = go.Figure(data=data, layout=layout)
	#fig.show()
visualizeDayofWeekData(getFacebookData())


def writetoDatabase(dictionary):
	conn = sqlite3.connect('206_APIsAndDBs.sqlite') #establish connect
	cur = conn.cursor() #define cursor 
	cur.execute('DROP TABLE IF EXISTS Users') #so you can run program multiple times
	cur.execute('CREATE TABLE Users (user_id INTEGER NOT NULL PRIMARY KEY, screen_name TEXT, num_favs INTEGER, description TEXT)') #create table


	