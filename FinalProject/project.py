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
import private_tokens2 as tokens

#cache set up 

CACHE_FNAME = "final_project_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r') #open your file to read in data from cache file 
	cache_contents = cache_file.read() #read the cache file
	cache_file.close() #close file
	CACHE_DICTION = json.loads(cache_contents) #load file string into json dictionary
except:
    CACHE_DICTION = {}

## INPUT: N/A. No input.
## OUTPUT: Return dictionary with all the data returned from facebook api on users last 100 posts
def getFacebookData():
	#check cache file for data
	#if yes return the cache data
	if 'facebook' in CACHE_DICTION:
		print("using cache for Facebook data\n") 
		return CACHE_DICTION['facebook'] 

	#if not in cache,fetch data 
	else:
		print("fetching Facebook data\n") #let user know what is happening

		#check is there is a valid access token, if not request it now 
		access_token = tokens.fb_access_token
		if access_token == None:
			print ("Please add your facebook access token to the private_tokens file or insert here:")
			access_token = input()
		#request facebook posts from user
		graph = facebook.GraphAPI(access_token)
		
		all_fields = ['created_time', 'place']
		all_fields = ','.join(all_fields)
		posts = graph.get_connections('me','posts', fields = all_fields, limit = 100) 

		#put in cache dictionary 
		CACHE_DICTION['facebook'] =  posts['data'] #put in cache dictionary 
		fw = open(CACHE_FNAME,"w") #open file
		fw.write(json.dumps(CACHE_DICTION)) #write results into cache file 
		fw.close()

		#return the results 
		print ('Facebook data cached\n')
		return posts['data']
	# profile = graph.get_object('me', fields = 'name,location{location}') #fields is an optional key word argument
	#return json.dumps(data)

## INPUT: N/A. No input.
## OUTPUT: Return dictionary with  data returned from instagram api on users last 20 posts
def getInstagramData():
	#check cache file for data
	#if yes return the cache data
	if 'instagram' in CACHE_DICTION:
		print("using cache for Instagram data\n") 
		return CACHE_DICTION['instagram'] 
	else:
		print("fetching Instagram data\n") #let user know what is happening

		#check is there is a valid access token, if not request it now 
		access_token =tokens.insta_access_token
		if access_token == None:
			print ("Please add your Instagram access token to the private_tokens file or insert here:\n")
			access_token = input()

		#request instagram posts from user	
		url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token=%s' %access_token
		response = requests.get(url)

		#parse response to extract the data needed  (latitude, longitude) of each post
		locations = []
		for post in json.loads(response.text)['data']:
			if post['location']:
				post_id = post['id']
				lat = float(post['location']['latitude'])
				lon = float(post['location']['longitude'])
				locations.append((post_id,lat,lon))

		#aput in cache dictionary 
		CACHE_DICTION['instagram'] =  locations #put in cache dictionary 
		fw = open(CACHE_FNAME,"w") #open file
		fw.write(json.dumps(CACHE_DICTION)) #write results into cache file 
		fw.close()
		#return data 
		print ('Instagram data cached\n')
		return locations

## INPUT: date in Facebook return format  .
## OUTPUT: Return day of week
def datetimetoDay(datetimedata):
	#extract date from string and change to datetime variable
	date = re.findall('([0-9]*-[0-9]*-[0-9]*)T',datetimedata)
	change = datetime.datetime.strptime(date[0], '%Y-%m-%d')
	#get dayofweek integer
	day = change.isoweekday()
	#retyrn string with day of week 
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
			
## INPUT: two dictionaries, instagram data and facebook data 
## OUTPUT: no return value, but new html file created in folder with locations of posts plotted 
	#instagram posts are purple and facebook posts are blue
def gmaps(instaresults, fbresults):
	#initialize map center on lat,long given
	gmap = gmplot.GoogleMapPlotter(33.0858, 39.29465, 3)
	lats = []
	longs = []

	#extract lat, long for each post from instagram (add to list)
	for post in instaresults:
		lats.append(post[1])
		longs.append(post[2])
	#plot location of instagram posts in purple
	gmap.scatter(lats, longs, 'purple', size=25)

	lats = []
	longs = []

	#extract lat, long for each post from facebook that has that data(add to list)
	for post in fbresults:
		if 'place' in post:
			lats.append(post['place']['location']['latitude'])
			longs.append(post['place']['location']['longitude'])

	#plot location of facebook posts in blue
	gmap.scatter(lats, longs, 'blue', size=25)
	#write to file
	gmap.draw("mymap.html")
	print ('A visualization of the location of your Facebook and Instagram posts has been created, check the local folder for mymap.html file.\n')


## INPUT: dictionary with facebook data.
## OUTPUT: No return value, but check plotly account for new bar graph 
def visualizeDayofWeekData(facebook_posts):
	#add plotly credentials 
	username = tokens.plotly_username
	api_key = tokens.plotly_api_key
	if username == None:
		print ("Please add your Plotly username to the private_tokens file or insert here:\n")
		username = input()
	if api_key == None:
		print ("Please add your Plotly API key to the private_tokens file or insert here:\n")
		api_key = input()

	#ser credentials
	plotly.tools.set_credentials_file(username=username, api_key=api_key)
	
	#create dictionary with number of posts per day from facebook posts
	day_count = {}
	for post in facebook_posts:
		day = datetimetoDay(post["created_time"])
		day_count[day] = day_count.get(day, 0) + 1
	
	days = []
	counts = []
	#turn dictionary into two list that will act as x-day,y-count values in bar chart
	for day, count in day_count.items():
		days.append(day)
		counts.append(count)
	#plot the data formated above using plotly 
	layout = go.Layout(title='Facebook Usage By Day')
	data = [go.Bar(x = days,y = counts)]
	fig = dict(data = data, layout = layout)
	py.iplot(fig, file_id='basic-bar',)
	#check account to see plot
	print ('A visualization of Facebook post frequency has been created, check your plotly account to see.\n')



conn = sqlite3.connect('FBandInsta.sqlite') #establish connect with SQLite
cur = conn.cursor() #define cursor 

#make request for facebook data
facebook_posts = getFacebookData()

cur.execute('DROP TABLE IF EXISTS Facebook') #so you can run program multiple times
#create facebook table
cur.execute('CREATE TABLE Facebook (post_id TEXT NOT NULL PRIMARY KEY, time_posted DATETIME, latitude FLOAT, longitude FLOAT)') 

#write facebook data into SQL Tavble
for post in facebook_posts:
	date = re.findall('([0-9]*-[0-9]*-[0-9]*)T',post['created_time'])
	change = datetime.datetime.strptime(date[0], '%Y-%m-%d')
	if 'place' in post:
		lat = post['place']['location']['latitude']
		lon = post['place']['location']['longitude']
	else:
		lat = None
		lon = None
	cur.execute("INSERT INTO Facebook (post_id, time_posted, latitude, longitude) VALUES (?,?,?,?)", (str(post['id']), change, lat, lon))

conn.commit() #commit changes to sql file
print ('Facebook data has been added to Facebook Table in FBandInsta SQL database.\n')

#visualize Facebook data into bar chart that shows frequency of posts per day
visualizeDayofWeekData(facebook_posts)

#make request for instagram data
instagram_posts = getInstagramData()

cur.execute('DROP TABLE IF EXISTS Instagram')#so you can run program multiple times
#create instagram table
cur.execute('CREATE TABLE Instagram (post_id TEXT NOT NULL PRIMARY KEY, latitude FLOAT, longitude FLOAT)')

#write instagram data into SQL Tavble
for post in instagram_posts:
	cur.execute("INSERT INTO Instagram (post_id, latitude, longitude) VALUES (?,?,?)", post)

conn.commit() #commit changes to sql file
print ('Instagram data has been added to Instagram Table in FBandInsta SQL database.\n')

#visualize Instagram abd Facebook data into a map that shows location of posts (social media is separated by color)
gmaps(instagram_posts, facebook_posts)



	