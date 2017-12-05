##Name:Julie Burke

## SI 206 2017
## Project 3
import unittest
import requests
import facebook  #pip install facebook-sdk
import json
import sqlite3
import datetime
import re
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import googlemaps
import gmplot


CACHE_FNAME = "final_project_cache.json"
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
		access_token = 'EAACEdEose0cBAOX1h5juTCRfAi2z9lYoTXHLpgOWV3BdMl0DyFBobyDOHBPM9RZCnXIxvo8JZCXxnNZCFbfF3qNoTMgNwCP5tQFZBAz4OLaGFif6tFWcGjqxSsXGzZB0SpdvlXtBtWY5MZAJ8qUOGd3bccysl5cfWlg4LhFuKwzEkcSzv0ZCwtRGtXNIHVcroH0AZBPhnZBNfGAZDZD'
		graph = facebook.GraphAPI(access_token)
		
		all_fields = ['created_time']
		day_count = {}
		#all_fields = ','.join(all_fields)
		#data = graph.get_connections('me','user_work_history') 
		posts = graph.get_connections('me','posts', fields = all_fields, limit = 100) 
		
		CACHE_DICTION['facebook'] =  posts['data'] #put in cache dictionary 
		fw = open(CACHE_FNAME,"w") #open file
		fw.write(json.dumps(CACHE_DICTION)) #write results into cache file 
		fw.close()
		return posts['data']
	# profile = graph.get_object('me', fields = 'name,location{location}') #fields is an optional key word argument
	#return json.dumps(data)

def getInstagramData():
	#from instagram.client import InstagramAPI
	data = []
	client_id = "1b5f1a1cb43046979f5d7176a9338a0f"
	client_secret = "50093b46a5be47b996101ed15c66b222 "
	access_token ='53913195.1b5f1a1.d6cf6e96d02745bb82bec42f6c07de80'
	#api = InstagramAPI(access_token = access_token, client_id= client_id,client_secret=client_secret)
	#recent = api.user_recent_media(user_id="53913195", count=100, fields = 'location')
	#print (type(recent[0]))
	url = 'https://api.instagram.com/v1/users/self/media/recent/?count=100/?access_token=53913195.1b5f1a1.d6cf6e96d02745bb82bec42f6c07de80'
	response = requests.get(url)
	print (response.text)
	locations = []
	for post in json.loads(response.text)['data']:
		if post['location']:
			post_id = post['id']
			lat = float(post['location']['latitude'])
			lon = float(post['location']['longitude'])
			locations.append((post_id,lat,lon))
	CACHE_DICTION['instagram'] =  locations #put in cache dictionary 
	fw = open(CACHE_FNAME,"w") #open file
	fw.write(json.dumps(CACHE_DICTION)) #write results into cache file 
	fw.close()
	return locations
	#for i in [1]:# range(5):
	#	response = requests.get(url)
	#	formatdata =  json.loads(response.text)
	#	print (formatdata)
	#	print (len(formatdata['data']))
	#	data.append(formatdata['data'])
	#	url = formatdata['pagination']#['next_url']
	#	print (url)

def datetimetoDay(datetimedata):
	date = re.findall('([0-9]*-[0-9]*-[0-9]*)T',datetimedata)
	change = datetime.datetime.strptime(date[0], '%Y-%m-%d')
	day = change.isoweekday()
	if day == 1:
		return'Monday'
	if day == 2:
		return 'Tuesday'
	if day == 3:
		return 'Wednesday'
	if day == 4:
		return 'Thursday'
	if day == 5:
		return 'Friday'
	if day == 6:
		return 'Saturday'
	if day == 7:
		return 'Sunday'
			


def visualizeDayofWeekData(facebook_posts):
	plotly.tools.set_credentials_file(username='julieburke', api_key='EnRYcjJL5LUMtyi8Zt5Q')
	day_count = {}
	for post in facebook_posts:
		day = datetimetoDay(post["created_time"])
		day_count[day] = day_count.get(day, 0) + 1

	layout = go.Layout(title='Facebook Usage By Day')
	data = [go.Bar(x = days,y = counts)]
	py.iplot(data, file_id='basic-bar')
	#fig = go.Figure(data=data, layout=layout)
	#fig.show()

facebook_posts = getFacebookData()

conn = sqlite3.connect('FBandInsta.sqlite') #establish connect
cur = conn.cursor() #define cursor 
cur.execute('DROP TABLE IF EXISTS Facebook') #so you can run program multiple times
cur.execute('CREATE TABLE Facebook (post_id TEXT NOT NULL PRIMARY KEY, time_posted DATETIME)') #create table

for post in facebook_posts:
	date = re.findall('([0-9]*-[0-9]*-[0-9]*)T',post['created_time'])
	change = datetime.datetime.strptime(date[0], '%Y-%m-%d')
	cur.execute("INSERT INTO Facebook (post_id, time_posted) VALUES (?,?)", (str(post['id']), change))

conn.commit() #commit changes to sql file


instagram_posts = getInstagramData()

cur.execute('DROP TABLE IF EXISTS Instagram')#so you can run program multiple times
cur.execute('CREATE TABLE Instagram (post_id TEXT NOT NULL PRIMARY KEY, latitude FLOAT, longitude FLOAT)')

for post in instagram_posts:
	cur.execute("INSERT INTO Instagram (post_id, latitude, longitude) VALUES (?,?,?)", post)
conn.commit() #commit changes to sql file

def gmaps(results):
	gmap = gmplot.GoogleMapPlotter(33.0858, 39.29465, 3)
	lats = []
	longs = []
	for post in results:
		lats.append(post[1])
		longs.append(post[2])
	gmap.scatter(lats, longs, 'purple', size=25)
	gmap.draw("mymap.html")
	gmap.heatmap(lats, longs)
	gmap.draw("mymap2.html")
gmaps(instagram_posts)



	