####################################################################################################
# Setting up imports

import os, sys
try:
	path = os.getcwd().split("?\\")[1].split('Plug-in Support')[0]+"Plug-ins\MOVIE2K.bundle\Contents\Services\URL\MOVIE2K\Modules"
except:
	path = os.getcwd().split("Plug-in Support")[0]+"Plug-ins/MOVIE2K.bundle/Contents/Services/URL/MOVIE2K/Modules"
sys.path.append(path)

try:
	import requests
except:
	import requests25 as requests

import urllib
import re
import time
import socket
import httplib
import random
import HostServices
from HostServices import StripArray
from HostServices import LoadData
from HostServices import JsonWrite

# Import SocksiPy
import sockschain as socks
def DEBUG(msg): Log(msg)
socks.DEBUG = DEBUG

# Random User Agent
UserAgent = ['Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Opera/9.25 (Windows NT 6.0; U; ja)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 2000) Opera 6.01 [ja]', 'Mozilla/5.0 (Windows; U; Windows NT 5.0; ja-JP; m18) Gecko/20010131 Netscape6/6.01', 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/85.7 (KHTML, like Gecko) Safari/85.7']
UserAgentNum = random.randrange(0, len(UserAgent)-1, 1)

# Movie2k Plugin Version
Version = "1.4.5"

# Set up Host Services
HostServices.Version = Version
HostServices.DEBUG = DEBUG
HostServices.UserAgent = UserAgent[UserAgentNum]

PREFIX         = "/video/movie2k"
NAME           = "Movie2k"
ART            = "art-default.jpg"
ICON           = "icon-default.png"
MOVIE2K_URL    = Prefs['movie2k_url']
CAPTCHA_DATA   = "captcha.data.json"
FAVORITES_DATA = "favorites.data.json"


####################################################################################################
def Start():

	# Initialize the plug-in
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

	# Setup the default attributes for the ObjectContainer
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	ObjectContainer.view_group = "InfoList"


	# Setup the default attributes for the other objects
	DirectoryObject.thumb = R(ICON)
	VideoClipObject.thumb = R(ICON)

	# Set the default cache time
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = UserAgent[UserAgentNum]

        
####################################################################################################
def DisableAdult():

	CheckAdult = Prefs['disabledadult']

	if CheckAdult == 'Disabled':
		return  False
	else:
		return True


####################################################################################################
def GetLanguage():

	CheckLang = Prefs['movie2k_language']

	return CheckLang


####################################################################################################
@handler(PREFIX, NAME, art = ART, thumb = ICON)
def MainMenu():

	# Enable Tor Proxy
	EnableTorConnect()

	# INitialize My Movie2k Login
	loginResult = Movie2kLogin()
	Log("Login success: " + str(loginResult))

	ICON_MOVIES  = "icon-movies.png"
	MOVIES_TITLE = "Movies"
	MOVIES_SUMMARY = "Your Movie and Blockbuster database!"
	MOVIES_THUMB = R(ICON_MOVIES)
	ICON_TVSHOWS = "icon-tvshows.png"
	TV_SHOWS_TITLE = "TV Shows"
	TV_SHOWS_SUMMARY = "Your TV Shows database!"
	TV_SHOWS_THUMB = R(ICON_TVSHOWS)
	ICON_MOVIES  = "icon-xxx movies.png"
	XXXMOVIES_TITLE = "XXX Movies"
	XXXMOVIES_SUMMARY = "Your XXX Movies database!"
	XXXMOVIES_THUMB = R(ICON_MOVIES)
	ICON_SEARCH = "icon-search.png"
	SEARCH_TITLE = "Search the Database"
	SEARCH_SUMMARY ="Find a TV Show or Movie from the Movie2k database!"
	SEARCH_THUMB = R(ICON_SEARCH)
	ICON_TRAILERSEARCH = "icon-trailer-addict.png"
	TRAILERSEARCH_TITLE = "Search for Your Daily Dose of Hi-Res Movie Trailers"
	TRAILERSEARCH_SUMMARY ="Find a Movie Trailer from the Trailer Addict database!"
	TRAILERSEARCH_THUMB = R(ICON_TRAILERSEARCH)
	ICON_PREFS = "icon-preferences.png"
	PREFS_TITLE = "Preferences"
	PREFS_SUMMARY = "Update login and channel information!"
	PREFS_THUMB = R(ICON_PREFS)
	ICON_MYMOVIE2k = "icon-mymovie2k.png"
	MYMOVIE2K_TITLE = "My Movie2k"
	MYMOVIE2K_SUMMARY = "List my links and Inbox on Movie2k!"
	MYMOVIE2K_THUMB = R(ICON_MYMOVIE2k)

	oc = ObjectContainer()
	
	oc.add(DirectoryObject(key=Callback(Movies, title=MOVIES_TITLE, type='Movies'), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
	oc.add(DirectoryObject(key=Callback(TVShows, title=TV_SHOWS_TITLE, type='TV Shows'), title=TV_SHOWS_TITLE, summary=TV_SHOWS_SUMMARY, thumb=TV_SHOWS_THUMB))
	if DisableAdult():
		oc.add(DirectoryObject(key=Callback(Movies, title=XXXMOVIES_TITLE, type='XXX Movies'), title=XXXMOVIES_TITLE, summary=XXXMOVIES_SUMMARY, thumb=XXXMOVIES_THUMB))
	oc.add(DirectoryObject(key = Callback(MyMovie2k, title=MYMOVIE2K_TITLE), title=MYMOVIE2K_TITLE, summary=MYMOVIE2K_SUMMARY, thumb=MYMOVIE2K_THUMB))
	oc.add(InputDirectoryObject(key=Callback(Search), title=SEARCH_TITLE, summary=SEARCH_SUMMARY, prompt="Search for", thumb=SEARCH_THUMB))
	oc.add(InputDirectoryObject(key=Callback(SearchTrailers), title=TRAILERSEARCH_TITLE, summary=TRAILERSEARCH_SUMMARY, prompt="Search for", thumb=TRAILERSEARCH_THUMB))
	#oc.add(SearchDirectoryObject(identifier="com.plexapp.plugins.movie2k", title=TRAILERSEARCH_TITLE, prompt=TRAILERSEARCH_SUMMARY, thumb=TRAILERSEARCH_THUMB))
	oc.add(PrefsObject(title=PREFS_TITLE, summary=PREFS_SUMMARY, thumb=PREFS_THUMB))

	return oc


####################################################################################################  
def Movie2kLogin():

	username = Prefs["username"]
	password = Prefs["password"]
	cookiejar = {"xxx2": "ok", "domain": ".movie4k.to", "path": "/", "onlylanguage": "", "lang": "en"}
	Dict['_movie2k_uid'] = cookiejar
	HTTP.Headers['Cookie'] = cookiejar

	if (username != None) and (password != None):
		try:
			files = {}
			cookies = {}
			session = requests.session()
			url = "http://" + MOVIE2K_URL + "/login.php?ua=login"
			authentication_values = {"username": username, "password": password}
			authentication_headers = {"Host": MOVIE2K_URL, "Referer": url, "User-Agent": UserAgent[UserAgentNum]}
			req = session.post(url, data=authentication_values, headers=authentication_headers, files=files, allow_redirects=True)
			data = req.content.split('<div id="maincontent4">')[1].split('<STRONG>')[1].split('</STRONG>')[0]

			if data == "Logged in!":			
				for key, value in session.cookies.items():
					cookies[key] = value
				cookiejar.update(cookies)
				HTTP.Headers['Cookie'] = cookiejar
				Dict['_movie2k_uid'] = cookiejar
				return True
			else:
				return False
		except:
			return False
	else:
		return False


################################################################################
@route(PREFIX + '/Search')
def Search(query):

	#Search movie4k.to for movies using user input, and populate a list with the results

	# Create a container to hold the results
	oc = ObjectContainer(title2="Search Results")
	
	#AutoComplete = "http://" + MOVIE2K_URL + "/searchAutoCompleteNew.php?search=" + urllib.quote_plus(query)
	#AutoSearch = HTML.ElementFromURL(AutoComplete).xpath('//table/tr')

	#for SearchList in AutoSearch:
	#	MOVIES_TITLE = SearchList.xpath('./td/a')[0].text
		
	type = 'N/A'
	dateadd = 'N/A'
	url = 'http://' + MOVIE2K_URL + '/movies.php?list=search'
	payload = {'search': query}
	files = {}
	cookies = Dict['_movie2k_uid']
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'en-US,en;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Host': MOVIE2K_URL,
		'Origin': 'http://' + MOVIE2K_URL,
		'Referer': 'http://' + MOVIE2K_URL + '/movies.php?list=search',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': UserAgent[UserAgentNum]
		}

	SEARCH_PAGE = requests.post(url, data=payload, headers=headers, files=files, allow_redirects=True, cookies=cookies)

	try:
		GET_THUMB = SEARCH_PAGE.content.split('<TABLE id="tablemoviesindex">')[1].split('<script type="text/javascript">')[1]
	except:
		GET_THUMB = None

	Movie =  SEARCH_PAGE.content.split('<TABLE id="tablemoviesindex">')[1].split('<TR')

	i = 1
	while (i < len(Movie)):
		MOVIES_TD = Movie[i].split('id="tdmovies"')
		MOVIES_TITLE = re.sub('\t', '', MOVIES_TD[1].split('<a')[1].split('">')[1].split('</a>')[0]).replace('  ', '')
		try:
			MOVIES_YEAR = MOVIES_TD[2].split('<div')[8].split('>')[1].split('<')[0]
			if MOVIES_YEAR == "":
				MOVIES_YEAR = "N/A"
		except:
			MOVIES_YEAR = "N/A"

		try:
			LANGUAGE_URL = MOVIES_TD[5].split('src="')[1].split('"')[0]
			try:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
			except:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
		except:
			MOVIES_LANG = "N/A"
		MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the search line up on Movie2k."
		MOVIES_PAGE = MOVIES_TD[1].split('<a href="')[1].split('"')[0]
		try:
			MOVIES_THUMB = GET_THUMB.split(Movie[i].split('id="coverPreview')[1].split('"')[0])[1].split("img src='")[1].split("'")[0]
		except:
			MOVIES_THUMB = None

		MOVIES_HOST = MOVIES_TD[2].split('>')[3].split('</a')[0].replace(' ', '')
		if MOVIES_HOST == "downloadnow!":
			oc = MessageContainer("Search Error", "Search did not return any positive results.  Please try another key word search!")
		elif MOVIES_LANG == GetLanguage() or MOVIES_LANG == 'N/A' or GetLanguage() == 'All':
			oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		i += 1

	return oc


####################################################################################################
@route(PREFIX + '/MyMovie2k')
def MyMovie2k(title):

	oc = ObjectContainer(title2=title)

	# Attempt to login
	loginResult = Movie2kLogin()
	Log("My Movie2k Login success: " + str(loginResult))

	# User input instructions
	ICON_INSTRUCTIONS = "icon-instructions.png"
	INSTRUCTIONS_THUMB = R(ICON_INSTRUCTIONS)
	title = "Special Instructions for Roku Users"
	summary = "Click here to see special instructions necessary for Roku Users for password input."
	oc.add(DirectoryObject(key=Callback(RokuUsersMyFavorites, title=title), title=title, summary=summary, thumb=INSTRUCTIONS_THUMB))

	# My Uploads on Movie4k.to
	ICON_MYUPLOADS = "icon-myuploads.png"
	MYUPLOADS_THUMB = R(ICON_MYUPLOADS)
	title = "My Uploads"
	summary = "Show all online, offline, waiting and queued links!"
	oc.add(DirectoryObject(key = Callback(Queue, title=title, loginResult=loginResult), title=title, summary=summary, thumb=MYUPLOADS_THUMB))

	# My Messages on Movie4k.to
	ICON_MYMESSAGES = "icon-mymessages.png"
	MYMESSAGES_THUMB = R(ICON_MYMESSAGES)
	title = "My Messages"
	summary = "Show messages from your Inbox!"
	oc.add(DirectoryObject(key = Callback(Messages, title=title, loginResult=loginResult), title=title, summary=summary, thumb=MYMESSAGES_THUMB))

	# My Favorite Movie4k.to links
	ICON_MYFAVORITES = "icon-my-favorites.png"
	MYFAVORITES_THUMB = R(ICON_MYFAVORITES)
	title = "My Favorite Links"
	summary = "Show my favorite links from Movie2k!"
	oc.add(DirectoryObject(key = Callback(MyFavoriteURL, title=title), title=title, summary=summary, thumb=MYFAVORITES_THUMB))

	# Add Favorite Movie4k.to link
	ICON_ADDFAVORITE = "icon-add-favorite.png"
	ADDFAVORITE_THUMB = R(ICON_ADDFAVORITE)
	title = "Add Favorite Link"
	summary = "Add a favorite link from Movie2k!"
	prompt = "Add a favorite link from Movie2k!"
	oc.add(InputDirectoryObject(key=Callback(InputFavoriteURL, title=title), title=title, summary=summary, thumb=ADDFAVORITE_THUMB, prompt=prompt))

	# Delete Favorite Movie4k.to link
	ICON_DELETEFAVORITE = "icon-delete-favorite.png"
	DELETEFAVORITE_THUMB = R(ICON_DELETEFAVORITE)
	title = "Delete Favorite Links"
	summary = "Delete my favorite links from Movie2k!"
	oc.add(DirectoryObject(key = Callback(DeleteFavoriteURL, title=title), title=title, summary=summary, thumb=DELETEFAVORITE_THUMB))

	return oc


####################################################################################################
def RokuUsersMyFavorites(title):

	return ObjectContainer(header="Special Instructions for Roku Users", message="Inputting Movie4k URL, Roku users must be using version 2.6.6 of the Plex Roku Channel (currently the PlexTest channel). If you do not want to input the Movie4k URL via the Roku input screen you can use the online Rokue remote control.  It can be found at:  http://www.remoku.tv   WARNING: DO NOT DIRECTLY TYPE OR PASTE THE TEXT IN THE INPUT CAPTCHA SECTION USING ROKU PLEX CHANNELS 2.6.4. THAT VERSION USES A SEARCH INSTEAD OF ENTRY SCREEN AND EVERY LETTER OF THE TEXT YOU ENTER WILL PRODUCE A SUBMIT FORM ON EACH LETTER.")


####################################################################################################
@route(PREFIX + '/MyFavoriteURL')
def MyFavoriteURL(title):

	oc = ObjectContainer(title2=title)

	hosts = LoadData(fp=FAVORITES_DATA, GetJson=False)
	i = 1
	for gethost in hosts:
		MOVIES_PAGE = gethost[i]['SiteURL']
		MOVIES_THUMB = gethost[i]['ThumbURL']
		MOVIES_TITLE = gethost[i]['Title']
		MOVIES_SUMMARY = gethost[i]['Summary']
		MOVIES_YEAR = gethost[i]['Date']
		dateadd = 'N/A'
		type = 'N/A'
		i += 1

		if MOVIES_PAGE != "":
			oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
	
	if len(oc) < 1:
		oc = ObjectContainer(header="Sorry", message="This section does not contain any My Favorite videos.  Please add a video to view.")

	return oc

####################################################################################################
@route(PREFIX + '/InputFavoriteURL')
def InputFavoriteURL(title, query):

	oc = ObjectContainer(title2=title)
	try:
		checkURL = query.split('/')[2]
		if checkURL != 'www.movie4k.to' and checkURL != 'www.movie2kproxy.org' and checkURL != 'www.movie2kproxy.com' and checkURL != '91.202.63.145':
			return ObjectContainer(header="Not a Movie4k URL", message="The entered URL is not a valid Movie4k video URL. Example of a valid Movie4k video URL: http://www.movie4k.to/Oblivion-watch-movie-3777965.html  Please try again and click Ok to exit this screen.")
	except:
		return ObjectContainer(header="Not a Movie4k URL", message="The entered URL is not a valid Movie4k video URL. Example of a valid Movie4k video URL: http://www.movie4k.to/Oblivion-watch-movie-3777965.html  Please try again and click Ok to exit this screen.")

	try:
		Num = query.split('-')
		checkNum = Num[len(Num)-1].split('.')[0]
		if len(checkNum) != 7:
			return ObjectContainer(header="Not a Valid Video Link", message="The entered URL is not a valid Movie4k video URL. Example of a valid Movie4k video URL: http://www.movie4k.to/Oblivion-watch-movie-3777965.html  Please try again and click Ok to exit this screen.")
	except:
		return ObjectContainer(header="Not a Valid Video Link", message="The entered URL is not a valid Movie4k video URL. Example of a valid Movie4k video URL: http://www.movie4k.to/Oblivion-watch-movie-3777965.html  Please try again and click Ok to exit this screen.")

	MOVIE_PAGE_HTML = HTML.ElementFromURL(query)
	MOVIE_INFO = MOVIE_PAGE_HTML.xpath('//div[@id="details"]')[0].text_content()
	try:
		date = re.sub('[^0-9]', '', MOVIE_INFO.split('Land/Year: ')[1])
		if date == "":
			date =  "0001"
	except:
		re.sub('[^0-9]', '', MOVIE_INFO.split('Land/Jahr: ')[1])
		if date == "":
			date =  "0001"

	MOVIE_INFO = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')
	MOVIES_LANG = GetLang(lang=MOVIE_INFO[1].xpath("./span/img")[0].get('src').split('.')[0])
	MOVIES_TITLE = MOVIE_INFO[1].xpath("./span/h1/a")[0].text.strip()
	MOVIES_QUALITY = MOVIE_INFO[1].xpath("./span/span/img")[0].get('title').split(' ')[2]
	MOVIES_THUMB = MOVIE_INFO[0].xpath("./a/img")[0].get('src')

	MOVIES_SUMMARY = "Year: "+date+" | Lang: "+MOVIES_LANG+" | Quality: "+MOVIES_QUALITY

	hosts = LoadData(fp=FAVORITES_DATA, GetJson=False)
	numHosts = len(hosts)
	i = 1
	jj = 0
	while jj <= numHosts:
		try:
			if hosts[jj][i]['SiteURL'] == "":
				hosts[jj][i]['SiteURL'] = query
				hosts[jj][i]['ThumbURL'] = MOVIES_THUMB
				hosts[jj][i]['Title'] = MOVIES_TITLE
				hosts[jj][i]['Summary'] = MOVIES_SUMMARY
				hosts[jj][i]['Date'] = date
				break
			else:
				i += 1
				jj += 1
		except:
			hosts.append({i : {'SiteURL': query, 'ThumbURL': MOVIES_THUMB, 'Title': MOVIES_TITLE, 'Summary': MOVIES_SUMMARY, 'Date': date}})
			break

	JsonWrite(fp=FAVORITES_DATA, jsondata=hosts)
	return ObjectContainer(header="Favorite URL Added", message="Your video URL from Movie4k has been added to MY FAVORITES line up now. Please click Ok to exit this screen.")


####################################################################################################
@route(PREFIX + '/DeleteFavoriteURL')
def DeleteFavoriteURL(title):

	oc = ObjectContainer(title2=title)

	hosts = LoadData(fp=FAVORITES_DATA, GetJson=False)
	i = 1
	for gethost in hosts:
		MOVIES_PAGE = gethost[i]['SiteURL']
		MOVIES_THUMB = gethost[i]['ThumbURL']
		MOVIES_TITLE = gethost[i]['Title']
		MOVIES_SUMMARY = gethost[i]['Summary']
		MOVIES_YEAR = gethost[i]['Date']
		i += 1

		if MOVIES_PAGE != "":
			oc.add(DirectoryObject(key=Callback(DeleteURL, title=MOVIES_TITLE, page=MOVIES_PAGE), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))

	if len(oc) < 1:
		oc = ObjectContainer(header="Sorry", message="This section does not contain any My Favorite videos to delete.")

	return oc


####################################################################################################
@route(PREFIX + '/DeleteURL')
def DeleteURL(title, page):

	oc = ObjectContainer(title2=title)

	hosts = LoadData(fp=FAVORITES_DATA, GetJson=False)
	i = 1
	for gethost in hosts:
		if gethost[i]['SiteURL'] == page:
			gethost[i]['SiteURL'] = ""
			gethost[i]['ThumbURL'] = ""
			gethost[i]['Title'] = ""
			gethost[i]['Summary'] = ""
			gethost[i]['Date'] = ""
			break
		else:
			i += 1

	JsonWrite(fp=FAVORITES_DATA, jsondata=hosts)
	return ObjectContainer(header="Deleted Movie4k URL", message="The Movie4k URL has been removed from My Favorites.  Please click Ok to exit this screen.")

####################################################################################################
@route(PREFIX + '/Queue')
def Queue(title, loginResult):

	if loginResult == "True":
		try:
			oc = ObjectContainer(title2=title)
			ICON_MYUPLOADS = "icon-myuploads.png"
			MYUPLOADS_THUMB = R(ICON_MYUPLOADS)
			MYUPLOADS_PAGE = "http://" + MOVIE2K_URL + "/ui.php?ua=myuploads&filter=no"
			TempMovie = None

			session_cookies = Dict['_movie2k_uid']
			session_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
			values = dict(session_token = Dict['_movie2k_uid'])
	
			req = requests.get(MYUPLOADS_PAGE, headers=session_headers, cookies=session_cookies)
			mylist = HTML.ElementFromString(req.content).xpath('//div[@id="maincontent4"]/table')[0]
			Movies = mylist.xpath('./tr')

			i = 1
			while i < len(Movies):
				Movie = Movies[i].xpath('./td/a')[0].text
				Host = strip_one_space(Movies[i].xpath('./td')[1].text_content())
				Status = Movies[i].xpath('./td')[2].text
				page = Movies[i].xpath('./td/a')[0].get('href')
				summary = "Hoster: "+Host+" | Status: "+Status
				title = "My Upload " + str(i) + ": " + Movie
		
				try:
					TitleParts = Movie.split(' ')
					TitleLen = len(TitleParts) - 1
					Season = int(TitleParts[TitleLen].split('S')[1].split('E')[0])
					Episode = int(TitleParts[TitleLen].split('E')[1])
					if Season >= 0 and Episode >= 0:
						type = 'TV Shows'
				except:
					type = 'Movies'

				if Movie != TempMovie:
					MOVIE_PAGE_HTML = HTML.ElementFromURL("http://"+MOVIE2K_URL+"/"+page)

					GET_THUMB = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')[0]
					thumb = GET_THUMB.xpath('./a/img')[0].get('src')

				TempMovie = Movie

				oc.add(DirectoryObject(key = Callback(TheMovieListings, title=title, page=page, date='N/A', dateadd='N/A', thumb=thumb, type=type, PageOfHosts=0, Host=Host), title = title, summary=summary, thumb=thumb))
				i += 1
		except:
			oc = ObjectContainer(header="User Login Error", message="Your user login and password are correct but there has been an error connecting to the website user account.  Please click ok to exit this screen and the back button to refresh login data. (MAY TAKE SEVERAL TRIES)")
	else:
		oc = ObjectContainer(header="User Login Required", message="Please enter your Movie4k login username and password in Preferences.  If you do not have an account please go to www.movie4k.to and click the Register link at the very top of the page to create you a new account.")

	return oc


####################################################################################################
@route(PREFIX + '/Messages')
def Messages(title, loginResult):

	if loginResult == "True":
		try:
			oc = ObjectContainer(title2=title)
			ICON_MYMESSAGES = "icon-mymessages.png"
			MYMESSAGES_THUMB = R(ICON_MYMESSAGES)
			MYMESSAGES_PAGE = "http://" + MOVIE2K_URL + "/ui.php?ua=messages_inbox"

			session_cookies = Dict['_movie2k_uid']
			session_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
			values = dict(session_token = Dict['_movie2k_uid'])
	
			req = requests.get(MYMESSAGES_PAGE, headers=session_headers, cookies=session_cookies)
			inbox = HTML.ElementFromString(req.content).xpath('//div[@id="maincontent4"]/form')[3]
			Message = inbox.xpath('./table/tr')

			i = 1
			while i < len(Message):
				From = Message[i].xpath('./td')[1].text
				Date = Message[i].xpath('./td')[2].text
				Subject = Message[i].xpath('./td/a')[0].text
				url = "http://" + MOVIE2K_URL + "/" + Message[i].xpath('./td/a')[0].get('href')
				summary = "From: "+From+" | Date: "+Date+" | Subject: "+Subject
				summary2 = "Date: "+Date+" | Subject: "+Subject
				title = "Inbox - Message " + str(i)

				oc.add(DirectoryObject(key = Callback(ShowMessage, title=title, url=url, summary=summary2), title = title, summary=summary, thumb=MYMESSAGES_THUMB))
				i += 1
		except:
			oc = ObjectContainer(header="User Login Error", message="Your user login and password are correct but there has been an error connecting to the website user account.  Please click ok to exit this screen and the back button to refresh login data. (MAY TAKE SEVERAL TRIES)")
	else:
		oc = ObjectContainer(header="User Login Required", message="Please enter your Movie4k login username and password in Preferences.  If you do not have an account please go to www.movie4k.to and click the Register link at the very top of the page to create you a new account.")

	return oc


####################################################################################################
def ShowMessage(title, url, summary):

	session_cookies = Dict['_movie2k_uid']
	session_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	values = dict(session_token = Dict['_movie2k_uid'])
	
	req = requests.get(url, headers=session_headers, cookies=session_cookies)
	getbody = HTML.ElementFromString(req.content).xpath('//div[@id="maincontent4"]/form')[3]
	body = getbody.text_content()
	oc = MessageContainer(summary, body)

	return oc


####################################################################################################
@route(PREFIX + '/TVShow')
def TVShows(title, type):
	
	oc = ObjectContainer(title2=title)

	#Add Featured TV Show
	ICON_FEATURED = "icon-latest-featured.png"
	MOVIES_TITLE = "Featured TV Shows"
	MOVIES_SUMMARY = "Your Featured TV Shows in the Movie2k database!"
	MOVIES_THUMB = R(ICON_FEATURED)
	MOVIES_PAGE = "http://" + MOVIE2K_URL + "/tvshows_featured.php"
	oc.add(DirectoryObject(key=Callback(FeaturedTVShowsPageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	#Add Latest Updates TV Show
	Genre_Type = "Latest Updates"
	ICON_UPDATES = "icon-latest-updates.png"
	TVSHOW_TITLE = "Newly Added TV Shows"
	TVSHOW_SUMMARY = "Your Latest Updates to the TV Shows database!"
	TVSHOW_THUMB = R(ICON_UPDATES)
	TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/tvshows-updates"
	oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, genre=Genre_Type, type=type), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))

	#Add Alphabitical listing to TV Show
	ICON_ALPHA = "icon-alphabetical.png"
	TVSHOW_TITLE = "Alphabitical listing of the TV Shows"
	TVSHOW_SUMMARY = "Listings sorted by Alphabitical order of the TV Shows database!"
	TVSHOW_THUMB = R(ICON_ALPHA)
	TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/tvshows-all.html"
	oc.add(DirectoryObject(key=Callback(AlphabiticalTVShowsPageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, type=type), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))

	#Add Genre Pages to TV Page
	ICON_GENRE = "icon-genre.png"
	TVSHOW_TITLE = "Genre listing of TV Shows"
	TVSHOW_SUMMARY = "Listings sorted by Genre of the TV Shows database!"
	TVSHOW_THUMB = R(ICON_GENRE)
	TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/genres-tvshows.html"
	oc.add(DirectoryObject(key=Callback(GenreTVShowsPageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, type=type), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/AlphabiticalTVShowsPageAdd')
def AlphabiticalTVShowsPageAdd(title, page, type):

	oc = ObjectContainer(title2=title)

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)

	Alpha_Type = "Numerical"
	ICON_MOVIES = "icon-numerical.png"
	MOVIES_TITLE = "Numerical"+" "+type
	MOVIES_SUMMARY = "Your Numerical list of the Movie database!"
	MOVIES_THUMB = R(ICON_MOVIES)
	MOVIES_PAGE_PART = "/tvshows-all-1.html"
	
	MOVIES_PAGE = "http://" + MOVIE2K_URL + MOVIES_PAGE_PART

	oc.add(DirectoryObject(key=Callback(TVShowsList, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Alpha_Type, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	for AlphNumeric in HTML.ElementFromString(req.content).xpath('//div[@id="content"]/div[@id="boxgrey"]'):
		Alpha_Type = AlphNumeric.xpath('./a')[0].text
		ICON_MOVIES = "icon-"+Alpha_Type.lower()+".png"
		MOVIES_TITLE = Alpha_Type+" "+type
		MOVIES_SUMMARY = "Your "+Alpha_Type+" list of the "+type+" database!"
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE_PART = AlphNumeric.xpath('./a')[0].get('href').split("/")[4]

		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/" + MOVIES_PAGE_PART

		oc.add(DirectoryObject(key=Callback(TVShowsList, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Alpha_Type, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/GenreTVShowsPageAdd')
def GenreTVShowsPageAdd(title, page, type):

	oc = ObjectContainer(title2=title)

	NotSkip = True

	for Genre in HTML.ElementFromURL(page).xpath('//div[@id="content"]/table[@id="tablemovies"]/tr'):
		Genre_Type = Genre.xpath('./td[@id="tdmovies"]/a')[0].text
		ICON_MOVIES = "icon-"+Genre_Type.lower()+".png"
		MOVIES_TITLE = Genre_Type+" "+type
		MOVIES_SUMMARY = "Your "+Genre_Type+" TV Shows database!"
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/"+Genre.xpath('./td[@id="tdmovies"]/a')[0].get('href')

		if DisableAdult() != True and Genre_Type.lower() == 'adult':
			NotSkip = False

		if NotSkip:
			oc.add(DirectoryObject(key=Callback(TVShowsList, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
		else:
			NotSkip = True

	return oc


####################################################################################################
@route(PREFIX + '/TVShowsList')
def TVShowsList(title, page, genre, type):
	
	oc = ObjectContainer(title2=title)

	for List in HTML.ElementFromURL(page).xpath('//div[@id="maincontent4"]/table[@id="tablemoviesindex"]/tr'):
		MOVIES_TD = List.xpath('./td[@id="tdmovies"]')
		try:
			LANGUAGE_URL = MOVIES_TD[1].xpath("./img")[0].get('src')
			try:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
			except:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
		except:
			MOVIES_LANG = "N/A"
		ICON_MOVIES = "icon-"+genre.lower()+".png"
		MOVIES_TITLE = MOVIES_TD[0].xpath('./a')[0].text
		MOVIES_SUMMARY = "Lang: "+MOVIES_LANG+" | Part of the "+genre+" TV Show line up on Movie2k."
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/"+MOVIES_TD[0].xpath('./a')[0].get('href')

		if MOVIES_LANG == GetLanguage() or MOVIES_LANG == 'N/A' or GetLanguage() == 'All':
			oc.add(DirectoryObject(key=Callback(TVShowSeasons, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=genre, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/FeaturedTVShowsPage')
def FeaturedTVShowsPageAdd(title, page, type):
	
	oc = ObjectContainer(title2=title)
	
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)
	FEATURED_TVSHOW_PAGE = HTML.ElementFromString(req.content)
	dateadd = 'N/A'
	TVSHOWS_DIV = FEATURED_TVSHOW_PAGE.xpath('//div[@id="maincontenttvshow"]/div')
	TVShowsLength = len(TVSHOWS_DIV)
	i = 0

	while i < TVShowsLength:
		TVSHOW_PAGE = TVSHOWS_DIV[i].xpath("./a")[0].get('href')
		TVSHOW_THUMB = TVSHOWS_DIV[i].xpath("./a/img")[0].get('src')
		TVSHOW_TITLE = TVSHOWS_DIV[i].xpath("./a/img")[0].get('title')
		i += 1
		TVSHOW_YEAR = re.sub('[^0-9]', '', TVSHOWS_DIV[i].xpath('./div[@class="beschreibung"]/span')[0].text_content().split('| Country/Year: ')[1])
		LANGUAGE_URL = TVSHOWS_DIV[i].xpath("./h2//img")[0].get('src')
		try:
			TVSHOW_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
		except:
			TVSHOW_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
		TVSHOW_SUMMARY = "Year: "+TVSHOW_YEAR+" | Lang: "+TVSHOW_LANG+" | Part of the Featured TV Show line up on Movie2k."
		i += 2
		oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, date=TVSHOW_YEAR, dateadd=dateadd, thumbck=TVSHOW_THUMB, type=type), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=Callback(GetThumb, url=TVSHOW_THUMB)))

	return oc


####################################################################################################
@route(PREFIX + '/TVShowSeasons')
def TVShowSeasons(title, page, genre, type):
	
	oc = ObjectContainer(title2=title)

	for Seasons in HTML.ElementFromURL(page).xpath('//div[@id="maincontent4"]/table[@id="tablemoviesindex"]/tr'):
		MOVIES_TD = Seasons.xpath('./td[@id="tdmovies"]')
		try:
			LANGUAGE_URL = MOVIES_TD[1].xpath("./img")[0].get('src')
			try:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
			except:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
		except:
			MOVIES_LANG = "N/A"
		ICON_MOVIES = "icon-"+genre.lower()+".png"
		MOVIES_TITLE = re.sub('\t', '', MOVIES_TD[0].xpath('./a')[0].text).replace('  ', '').replace(',', ', ').replace(':', ': ')
		MOVIES_SUMMARY = "Lang: "+MOVIES_LANG+" | Part of the "+genre+" TV Shows season line up on Movie2k."
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/"+MOVIES_TD[0].xpath('./a')[0].get('href')

		oc.add(DirectoryObject(key=Callback(TVShowEpisodes, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=genre, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/TVShowEpisodes')
def TVShowEpisodes(title, page, genre, type):
	
	oc = ObjectContainer(title2=title)

	THUMB = 0

	for Episodes in HTML.ElementFromURL(page).xpath('//div[@id="maincontent4"]/table[@id="tablemoviesindex"]/tr'):
		MOVIES_TD = Episodes.xpath('./td[@id="tdmovies"]')
		try:
			LANGUAGE_URL = MOVIES_TD[4].xpath("./img")[0].get('src')
			try:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
			except:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
		except:
			MOVIES_LANG = "N/A"
		DATE_ADDED = MOVIES_TD[3].text
		ICON_MOVIES = "icon-"+genre.lower()+".png"
		MOVIES_TITLE = re.sub('\t', '', MOVIES_TD[0].xpath('./a')[0].text).replace('  ', '').replace(',', ', ').replace(':', ': ')
		MOVIES_SUMMARY = "Added: "+DATE_ADDED+" | Lang: "+MOVIES_LANG+" | Part of the "+genre+" TV Shows episode line up on Movie2k."
		MOVIES_PAGE = MOVIES_TD[0].xpath('./a')[0].get('href')
		if THUMB == 0:
			GET_THUMB = HTML.ElementFromURL("http://"+MOVIE2K_URL+"/"+MOVIES_PAGE).xpath('//div[@id="maincontent5"]/div/div')[0]
			MOVIES_THUMB = GET_THUMB.xpath('./a/img')[0].get('src')
			THUMB = 1

		oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=DATE_ADDED, dateadd=DATE_ADDED, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))

	return oc


####################################################################################################
@route(PREFIX + '/Movie')
def Movies(title, type):
	
	oc = ObjectContainer(title2=title)

	Genre_Type = "Latest Updates"
	ICON_UPDATES = "icon-latest-updates.png"

	if type == 'Movies':
		#Add Newly Added Cinema Movies Page
		ICON_CINEMA = "icon-cinema.png"
		MOVIES_TITLE = "Newly Added Cinema Movies"
		MOVIES_SUMMARY = "Your Latest Updates to the Cinema Movies database!"
		MOVIES_THUMB = R(ICON_CINEMA)
		if GetLanguage() == 'German':
			MOVIES_PAGE = "http://" + MOVIE2K_URL + "/index.php?lang=de"
		else:
			MOVIES_PAGE = "http://" + MOVIE2K_URL + "/index.php?lang=us"
		oc.add(DirectoryObject(key=Callback(CinemaMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		#Add Latest Updates Movie Page
		MOVIES_TITLE = "Newly Added Movies"
		MOVIES_SUMMARY = "Your Latest Updates to the Movies database!"
		MOVIES_THUMB = R(ICON_UPDATES)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/movies-updates"
		oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		#Add By Alphabitical listing Movie Page
		ICON_ALPHA = "icon-alphabetical.png"
		MOVIES_TITLE = "Alphabitical listing of Movies"
		MOVIES_SUMMARY = "Listings sorted by Alphabitical order of the Movies database!"
		MOVIES_THUMB = R(ICON_ALPHA)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/movies-all.html"
		oc.add(DirectoryObject(key=Callback(AlphabiticalPageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		#Add By Genre listing Movie Page
		ICON_GENRE = "icon-genre.png"
		MOVIES_TITLE = "Genre listing of Movies"
		MOVIES_SUMMARY = "Listings sorted by Genre of the Movies database!"
		MOVIES_THUMB = R(ICON_GENRE)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/genres-movies.html"
		oc.add(DirectoryObject(key=Callback(GenrePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	elif type == 'XXX Movies':
		ParentalLock = Prefs["parentallock"]
		ICON_PASSWORD = "icon-password.png"
		PARENTAL_THUMB = R(ICON_PASSWORD)
		ICON_INSTRUCTIONS = "icon-instructions.png"
		INSTRUCTIONS_THUMB = R(ICON_INSTRUCTIONS)
		Password = LoadData(fp=CAPTCHA_DATA)
		ParentalPassword = Password[0][1]['ParentalPassword']

		if ParentalLock == "Enabled" or (ParentalLock == "Disabled" and ParentalPassword != ""):
			if ParentalLock == "Enabled" and ParentalPassword == "":
				title = "Parental Lockout Enabled"
				summary = "Click here to input New Parental Lock password."
				prompt="Click here to input New Parental Lock password."
			elif ParentalLock == "Enabled" and ParentalPassword != "":
				title = "Parental Lockout"
				summary = "Click here to input Parental Lock password."
				prompt="Click here to input Parental Lock password."
			elif ParentalLock == "Disabled" and ParentalPassword != "":
				title = "Parental Lockout Disabled"
				summary = "Click here to input Parental Lock password to delete password."
				prompt="Click here to input Parental Lock password to delete password."

			#Add Password Check XXX Movie Page
			oc.add(DirectoryObject(key=Callback(RokuUsersPasswordInput, title="Special Instructions for Roku Users"), title="Special Instructions for Roku Users", thumb=INSTRUCTIONS_THUMB, summary="Click here to see special instructions necessary for Roku Users for password input."))
			oc.add(InputDirectoryObject(key=Callback(InputParentalPassword, title=title, type=type), title=title, summary=summary, thumb=PARENTAL_THUMB, prompt=prompt))
		else:

			#Add Featured XXX Movie Page
			ICON_FEATURED = "icon-latest-featured.png"
			PORN_TITLE = "Featured XXX Movies"
			PORN_SUMMARY = "Your Featured Movies in the XXX Movies database!"
			PORN_THUMB = R(ICON_FEATURED)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-updates.html"
			oc.add(DirectoryObject(key=Callback(FeaturedMoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add Latest Updates XXX Movie Page
			PORN_TITLE = "Newly Added XXX Movies"
			PORN_SUMMARY = "Your Latest Updates to the XXX Movies database!"
			PORN_THUMB = R(ICON_UPDATES)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-updates"
			oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, genre=Genre_Type, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add By Alphabitical listing XXX Movie Page
			ICON_ALPHA = "icon-alphabetical.png"
			PORN_TITLE = "Alphabitical listing of XXX Movies"
			PORN_SUMMARY = "Listings sorted by Alphabitical order of the XXX Movies database!"
			PORN_THUMB = R(ICON_ALPHA)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-all.html"
			oc.add(DirectoryObject(key=Callback(AlphabiticalPageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add By Genre listing XXX Movie Page
			ICON_GENRE = "icon-genre.png"
			PORN_TITLE = "Genre listing of XXX Movies"
			PORN_SUMMARY = "Listings sorted by Genre of the XXX Movies database!"
			PORN_THUMB = R(ICON_GENRE)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/genres-xxx.html"
			oc.add(DirectoryObject(key=Callback(GenrePageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/InputParentalPassword')
def InputParentalPassword(title, type, query):

	oc = ObjectContainer(title2=title)

	ParentalLock = Prefs["parentallock"]
	Password = LoadData(fp=CAPTCHA_DATA)
	ParentalPassword = Password[0][1]['ParentalPassword']
	PasswordCheck = ParentalPassword.decode('base64', 'strict')

	if ParentalLock == "Enabled" and ParentalPassword == "":
		Password[0][1]['ParentalPassword'] = query.encode('base64', 'strict')
		JsonWrite(fp=CAPTCHA_DATA, jsondata=Password)
		return ObjectContainer(header="Parental Lockout Enabled", message="The Parental Lock password has now been enabled. Please click Ok to exit this screen and then click the back button to refresh the menu line up.")
	elif ParentalLock == "Disabled" and ParentalPassword != "":
		if query != PasswordCheck:
			return ObjectContainer(header="Parental Lockout Error", message="The entered password does not match the one that has been set for Parental Lock!  Please Try Again!") 
		else:
			Password[0][1]['ParentalPassword'] = ""
			JsonWrite(fp=CAPTCHA_DATA, jsondata=Password)
			return ObjectContainer(header="Parental Lockout Diabled", message="The Parental Lock password has now been removed. Please click Ok to exit this screen and then click the back button to refresh the menu line up.")
	elif ParentalLock == "Enabled" and ParentalPassword != "":
		if query != PasswordCheck:
			return ObjectContainer(header="Parental Lockout Error", message="The entered password does not match the one that has been set for Parental Lock!  Please Try Again!") 
		else:

			#Add Featured XXX Movie Page
			ICON_FEATURED = "icon-latest-featured.png"
			PORN_TITLE = "Featured XXX Movies"
			PORN_SUMMARY = "Your Featured Movies in the XXX Movies database!"
			PORN_THUMB = R(ICON_FEATURED)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-updates.html"
			oc.add(DirectoryObject(key=Callback(FeaturedMoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add Latest Updates XXX Movie Page
			Genre_Type = "Latest Updates"
			ICON_UPDATES = "icon-latest-updates.png"
			PORN_TITLE = "Newly Added XXX Movies"
			PORN_SUMMARY = "Your Latest Updates to the XXX Movies database!"
			PORN_THUMB = R(ICON_UPDATES)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-updates"
			oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, genre=Genre_Type, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add By Alphabitical listing XXX Movie Page
			ICON_ALPHA = "icon-alphabetical.png"
			PORN_TITLE = "Alphabitical listing of XXX Movies"
			PORN_SUMMARY = "Listings sorted by Alphabitical order of the XXX Movies database!"
			PORN_THUMB = R(ICON_ALPHA)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-all.html"
			oc.add(DirectoryObject(key=Callback(AlphabiticalPageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add By Genre listing XXX Movie Page
			ICON_GENRE = "icon-genre.png"
			PORN_TITLE = "Genre listing of XXX Movies"
			PORN_SUMMARY = "Listings sorted by Genre of the XXX Movies database!"
			PORN_THUMB = R(ICON_GENRE)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/genres-xxx.html"
			oc.add(DirectoryObject(key=Callback(GenrePageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

	return oc


#####################################################################################################
# This is special instructions for Roku users
def RokuUsersPasswordInput(title):

	return ObjectContainer(header="Special Instructions for Roku Users", message="Inputting password, Roku users must be using version 2.6.6 of the Plex Roku Channel (currently the PlexTest channel). If the Parantal Lock has been enabled, please input the password to view the adult content.  If the Parental Lock has been disabled enter the password to delete the password.  WARNING: DO NOT DIRECTLY TYPE OR PASTE THE TEXT IN THE INPUT CAPTCHA SECTION USING ROKU PLEX CHANNELS 2.6.4. THAT VERSION USES A SEARCH INSTEAD OF ENTRY SCREEN AND EVERY LETTER OF THE TEXT YOU ENTER WILL PRODUCE A SUBMIT FORM ON EACH LETTER.")


####################################################################################################
@route(PREFIX + '/AlphabiticalPageAdd')
def AlphabiticalPageAdd(title, page, type):

	oc = ObjectContainer(title2=title)

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)

	Alpha_Type = "Numerical"
	ICON_MOVIES = "icon-numerical.png"
	MOVIES_TITLE = "Numerical"+" "+type
	MOVIES_SUMMARY = "Your Numerical list of the Movie database!"
	MOVIES_THUMB = R(ICON_MOVIES)
	if type == "Movies":
		MOVIES_PAGE_PART = "/movies-all-1-"
	else:
		MOVIES_PAGE_PART = "/xxx-all-1-"

	MOVIES_PAGE = "http://" + MOVIE2K_URL + MOVIES_PAGE_PART

	oc.add(DirectoryObject(key=Callback(MovieGenres, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Alpha_Type, thumb=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
	Page = HTML.ElementFromString(req.content).xpath('//div[@id="content"]/div[@id="content"]/div')[0]

	for AlphNumeric in Page.xpath('./div[@id="boxgrey"]'):
		Alpha_Type = AlphNumeric.xpath('./a')[0].text
		ICON_MOVIES = "icon-"+Alpha_Type.lower()+".png"
		MOVIES_TITLE = Alpha_Type+" "+type
		MOVIES_SUMMARY = "Your "+Alpha_Type+" list of the "+type+" database!"
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE_PART = AlphNumeric.xpath('./a')[0].get('href').split(".")[1]

		MOVIES_PAGE = "http://" + MOVIE2K_URL + MOVIES_PAGE_PART + "-"

		oc.add(DirectoryObject(key=Callback(MovieGenres, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Alpha_Type, thumb=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/GenrePageAdd')
def GenrePageAdd(title, page, type):

	oc = ObjectContainer(title2=title)

	NotSkip = True
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)

	for Genre in HTML.ElementFromString(req.content).xpath('//div[@id="content"]/table[@id="tablemovies"]/tr'):
		Genre_Type = Genre.xpath('./td[@id="tdmovies"]/a')[0].text
		ICON_MOVIES = "icon-"+Genre_Type.lower()+".png"
		MOVIES_TITLE = Genre_Type+" "+type
		MOVIES_SUMMARY = "Your "+Genre_Type+" "+type+" database!"
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE_PART = Genre.xpath('./td[@id="tdmovies"]/a')[0].get('href').split(Genre_Type.replace(' ','+'))[0]

		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/"+MOVIES_PAGE_PART

		if DisableAdult() != True and Genre_Type.lower() == 'adult':
			NotSkip = False

		if NotSkip:
			oc.add(DirectoryObject(key=Callback(MovieGenres, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, thumb=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
		else:
			NotSkip = True

	return oc


####################################################################################################
@route(PREFIX + '/MovieGenres')
def MovieGenres(title, page, genre, thumb, type):
	
	oc = ObjectContainer(title2=title)

	i = 1
	MOVIES = page+"1.html"
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(MOVIES, headers=headers, cookies=cookies)
	NUMPAGES = len(HTML.ElementFromString(req.content).xpath('//div[@id="maincontent4"]/div[@id="boxgrey"]')) + 1
	
	while i <= NUMPAGES:
		do = DirectoryObject()
		do.title = "Page "+str(i)+" - List of "+genre+" "+type
		do.key = Callback(MoviePageAdd, title=do.title, page=page+str(i), genre=genre, type=type)
		do.summary = "Page "+str(i)+" of the line up of "+genre+" "+type+" from Movie2k."
		do.thumb = thumb
		oc.add(do)

		i += 1

	return oc


####################################################################################################
@route(PREFIX + '/CinemaMoviePage')
def CinemaMoviePageAdd(title, page, type):
	
	oc = ObjectContainer(title2=title)
	
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)
	CINEMA_MOVIE_PAGE = HTML.ElementFromString(req.content)
	dateadd = 'N/A'

	for Movie in CINEMA_MOVIE_PAGE.xpath('//div[@id="maincontentnew"]/div'):
		try:	
			MOVIES_TD = Movie
			MOVIES_YEAR = time.strftime("%Y", time.localtime(time.time()))
			MOVIES_TITLE = MOVIES_TD.xpath("./a/img")[0].get('title').replace(' kostenlos','')
			MOVIES_PAGE = MOVIES_TD.xpath("./a")[0].get('href')
			MOVIES_THUMB = MOVIES_TD.xpath("./a/img")[0].get('src')
	
			if GetLanguage() == 'German':
				MOVIES_LANG = "German"
			else:
				MOVIES_LANG = "English"
			MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the Cinema Movies line up on Movie2k."

			oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))			
		except:
			pass

	for Movie in CINEMA_MOVIE_PAGE.xpath('//div[@id="maincontentnew"]/div'):
		try:	
			MOVIES_TD = Movie.xpath('./div')[0]
			MOVIES_YEAR = 'N/A'
			MOVIES_TITLE = MOVIES_TD.xpath("./a/img")[0].get('title').replace(' kostenlos','')
			MOVIES_PAGE = MOVIES_TD.xpath("./a")[0].get('href')
			MOVIES_THUMB = MOVIES_TD.xpath("./a/img")[0].get('src')
	
			if GetLanguage() == 'German':
				MOVIES_LANG = "German"
			else:
				MOVIES_LANG = "English"
			MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the Older Cinema Movies line up on Movie2k."

			oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		except:
			pass

	return oc


####################################################################################################
@route(PREFIX + '/FeaturedMoviePageAdd')
def FeaturedMoviePageAdd(title, page, type):

	oc = ObjectContainer(title2=title)
	
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)
	FEATURED_MOVIE_PAGE = HTML.ElementFromString(req.content)
	dateadd = 'N/A'

	i = 2
	while i <= 3:
		for Movie in FEATURED_MOVIE_PAGE.xpath('//div[@id="maincontent'+str(i)+'"]/div[@id="divnotinuse"]'):	
			MOVIES_TD = Movie.xpath('./div')[0]
			MOVIES_TITLE = MOVIES_TD.xpath("./a/img")[0].get('title')
			MOVIES_PAGE = MOVIES_TD.xpath("./a")[0].get('href')
			MOVIES_THUMB = MOVIES_TD.xpath("./a/img")[0].get('src')
			MOVIES_YEAR = time.strftime("%Y", time.localtime(time.time()))
			MOVIES_LANG = "English"
			MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the Featured XXX Movies line up on Movie2k."

			oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		i += 1

	return oc


####################################################################################################
@route(PREFIX + '/MovieGenrePage')
def MoviePageAdd(title, page, genre, type):
	
	oc = ObjectContainer(title2=title, view_group='InfoList')

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	GENRE_PAGE = page+".html"
	req = requests.get(GENRE_PAGE, headers=headers, cookies=cookies)

	GENRE_MOVIE_PAGE = HTML.ElementFromString(req.content)

	try:
		GET_THUMB = GENRE_MOVIE_PAGE.xpath('//div[@id="maincontent4"]/script')[0].text
	except:
		GET_THUMB = None

	for Movie in GENRE_MOVIE_PAGE.xpath('//div[@id="maincontent4"]/table[@id="tablemoviesindex"]/tr'):
		MOVIES_TD = Movie.xpath('./td[@id="tdmovies"]')
		MOVIES_TITLE = re.sub('\t', '', MOVIES_TD[0].xpath("./a")[0].text).replace('  ', '').replace(',', ', ').replace(':', ': ')
		if type == 'TV Shows':
			dateadd = MOVIES_TD[3].text
		else:
			dateadd = 'N/A'
		try:
			MOVIES_YEAR = MOVIES_TD[1].xpath("./div")[7].text
			if MOVIES_YEAR == None:
				MOVIES_YEAR = "N/A"
		except:
			MOVIES_YEAR = "N/A"

		try:
			LANGUAGE_URL = MOVIES_TD[4].xpath("./img")[0].get('src')
		except:
			LANGUAGE_URL = MOVIES_TD[2].xpath("./img")[0].get('src')

		try:
			try:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
			except:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
		except:
			MOVIES_LANG = "N/A"
		MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the "+genre+" "+type+" line up on Movie2k."
		MOVIES_PAGE = MOVIES_TD[0].xpath("./a")[0].get('href')
		try:
			MOVIES_THUMB = GET_THUMB.split(Movie.get('id'))[1].split("img src='")[1].split("'")[0]
		except:
			try:
				Log(MOVIES_PAGE)
				MOVIE_INFO = MOVIES_PAGE.split('.')[0].split('-')
				i = len(MOVIE_INFO)
				i = i - 1
				jj = 0
				THUMB_PART = MOVIE_INFO[i]
				while jj < i:
					THUMB_PART = THUMB_PART+'-'+MOVIE_INFO[jj]
					jj += 1
				MOVIES_THUMB = "http://" + MOVIE2K_URL + "/thumbs/cover-"+THUMB_PART+".jpg"
			except:
				MOVIES_THUMB = ""

		if MOVIES_LANG == GetLanguage() or MOVIES_LANG == 'N/A' or GetLanguage() == 'All':
			oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))

	return oc


####################################################################################################
@route(PREFIX + '/TVandMovieHostPage')
def SubMoviePageAdd(title, page, date, dateadd, thumbck, type):

	oc = ObjectContainer(title2=title)

	MOVIE_PAGE_HTML = HTML.ElementFromURL("http://"+MOVIE2K_URL+"/"+page)

	GET_THUMB = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')[0]
	thumb = GET_THUMB.xpath('./a/img')[0].get('src')

	if thumb.split('/')[4] == "noposter.gif":
		if thumbck != "" and thumbck != None:
			thumb = thumbck

	Listing = MOVIE_PAGE_HTML.xpath('//div[@id="menu"]//tr[@id="tablemoviesindex2"]')
	NumHostListing1 = len(Listing)
	StringListing = MOVIE_PAGE_HTML.xpath('//div[@id="menu"]//script[@type="text/javascript"]')
	NumStringListing = len(StringListing)
	NumHostListing2 = 0
	HostCount = 1
	nsl = 0
	sll = 1
	Num1 = 0
	Num2 = 0
	i = 1
	k = 0
	Hosts = ""

	while nsl < NumStringListing:
		NumHosts = len(StringListing[nsl].text.split('links[')) - 2
		Log("Len"+str(nsl)+": "+str(NumHosts)+" "+StringListing[nsl].text.split('links[')[1].split(']')[0]+" "+StringListing[nsl].text.split('links[')[2].split(']')[0]+" "+StringListing[nsl].text.split('links[')[3].split(']')[0])
		NumHostListing2 = NumHostListing2 + NumHosts
		nsl += 1

	p = (float(NumHostListing1)+float(NumHostListing2))/4.0 - (NumHostListing1+NumHostListing2)/4
	jj = (NumHostListing1+NumHostListing2)/4
	if p > 0:
		jj += 1

	while i <= jj:
		while HostCount <= 4:
			if Num1 < NumHostListing1:
				try:
					Host = Listing[Num1].xpath("./td/a/img")[0].get('title').split(' ')[0].split('.')[0].capitalize()
				except:
					Host = Listing[Num1].xpath("./td/a/img")[0].get('title').split(' ')[0].capitalize()
				Num1 += 1
				Hosts = Hosts + Host + ", "
			elif Num2 < NumHostListing2:
				ScriptListing = StringListing[k].text.split('links[')
				NumHosts = len(ScriptListing) - 2	
				try:
					Host = ScriptListing[sll].split('title=\\"')[1].split('\\"')[0].split(' ')[0].split('.')[0].capitalize()
				except:
					Host = ScriptListing[sll].split('title=\\"')[1].split('\\"')[0].split(' ')[0].capitalize()
				if sll == NumHosts:
					k += 1
					sll = 1
				else:
					sll += 1
				Num2 += 1
				Hosts = Hosts + Host + ", "
			else:
				HostCount = 4
			HostCount += 1

		MOVIES_SUMMARY = "Page - " + str(i) + " | Hosts: " + Hosts[:-2]
		oc.add(DirectoryObject(key=Callback(TheMovieListings, title=title, page=page, date=date, dateadd=dateadd, thumb=thumb, type=type, PageOfHosts=i), title=title, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=thumb)))
		HostCount = 1
		Hosts = ""
		i += 1

	return oc


####################################################################################################
@route(PREFIX + '/TVandTheMovieListings')
def TheMovieListings(title, page, date, dateadd, thumb, type, PageOfHosts, Host=None):

	oc = ObjectContainer(title2=title)

	MOVIE_PAGE_HTML = HTML.ElementFromURL("http://"+MOVIE2K_URL+"/"+page)
	MOVIE_INFO = MOVIE_PAGE_HTML.xpath('//div[@id="details"]')[0].text_content()
	source_title = "Movie2k"

	summary = MOVIE_PAGE_HTML.xpath('//div[@class="moviedescription"]')[0].text
	if summary.strip() == "":
		summary = "Description not given..."

	try:
		rating = float(MOVIE_PAGE_HTML.xpath('//div[@id="details"]/a')[0].text)
	except:
		rating = 0.0

	if date == "N/A":
		try:
			date = re.sub('[^0-9]', '', MOVIE_INFO.split('Land/Year: ')[1])
			if date == "":
				date =  "0001"
		except:
			re.sub('[^0-9]', '', MOVIE_INFO.split('Land/Jahr: ')[1])
			if date == "":
				date =  "0001"

	date = Datetime.ParseDate(date, "%Y")
	
	genres = []
	genre = MOVIE_INFO.split('Genre:')[1].split('|')[0]
	genres = StripArray(arraystrings=genre.split(','))

	try:
		try:
			duration = int(float(MOVIE_INFO.split('Length: ')[1].split(' minutes')[0])*60*1000)
		except:
			try:
				duration = int(float(MOVIE_INFO.split('nge: ')[1].split(' Minuten')[0])*60*1000)
			except:
				duration = int(float(MOVIE_INFO.split('nge: ')[1].split(' Minutes')[0])*60*1000)
	except:
		duration = None

	directors = []
	try:
		try:
			director = MOVIE_INFO.split('Director:')[1].split('|')[0]
			directors = StripArray(arraystrings=director.split(','))
		except:
			director = MOVIE_INFO.split('Regie:')[1].split('|')[0]
			directors = StripArray(arraystrings=director.split(','))
	except:
		director = 'Not Available'
		directors.append(director)

	guest_stars = []
	try:
		try:
			actors = MOVIE_INFO.split('Actors:')[1]
			guest_stars = StripArray(arraystrings=actors.split(','))
		except:
			actors = MOVIE_INFO.split('Schauspieler:')[1]
			guest_stars = StripArray(arraystrings=actors.split(','))
	except:
		actors = None

	try:
		try:
			content_rating = MOVIE_INFO.split('Rated ')[1].split(' ')[0]
		except:
			content_rating = MOVIE_INFO.split('MPAA: ')[1].split(' ')[0]
	except:
		try:
			movie_rating = MOVIE_INFO.split('Freigegeben ')[1].split(' Jahren')[0]
			if movie_rating == 'ab 0':
				content_rating = 'NR'
			elif movie_rating == 'ab 6':
				content_rating = 'G'
			elif movie_rating == 'ab 12':
				content_rating = 'PG'
			elif movie_rating == 'ab 16':
				content_rating = 'R'
			elif movie_rating == 'ab 18':
				content_rating = 'NC-17'
		except:
			content_rating = 'NR'

	try:
		subtitle = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')[1]
		try:
			season = int(subtitle.xpath('./span/h1/a/span')[0].text.split('Season ')[1].split(',')[0].replace(' ', ''))
			index = int(subtitle.xpath('./span/h1/a/span')[0].text.split('Episode ')[1].replace(' ', ''))
		except:
			season = int(subtitle.xpath('./span/h1/a')[0].text.split('Staffel ')[1].split(',')[0].replace(' ', ''))
			index = int(subtitle.xpath('./span/h1/a')[0].text.split('Episode ')[1].replace(' ', ''))
		if type == 'N/A':
			type = 'TV Shows'
	except:
		season = 0
		index = 0
		if type == 'N/A':
			type = 'Movies'

	Listing = MOVIE_PAGE_HTML.xpath('//div[@id="menu"]//tr[@id="tablemoviesindex2"]')
	StringListing = MOVIE_PAGE_HTML.xpath('//div[@id="menu"]//script[@type="text/javascript"]')
	NumHostListing1 = len(Listing)
	NumStringListing = len(StringListing)
	NumHostListing2 = 0
	CreatePage = True
	CurrentPage = 1
	HostCountTotal = 1
	HostCount = 1
	nsl = 0
	sll = 1
	i = 0
	k = 0
	jj = 0

	while nsl < NumStringListing:
		NumHosts = len(StringListing[nsl].text.split('links[')) - 2
		NumHostListing2 = NumHostListing2 + NumHosts
		nsl += 1

	p = (float(NumHostListing1)+float(NumHostListing2))/4.0 - (NumHostListing1+NumHostListing2)/4
	NumPages = (NumHostListing1+NumHostListing2)/4
	if p > 0:
		NumPages += 1

	TotalHosts = NumHostListing1 + NumHostListing2

	Log("Listing Length: "+str(NumHostListing1))
	Log("Listing Script Length: "+str(NumStringListing))
	Log("Number of Pages: "+str(NumPages))
	Log("Total Hosts: "+str(TotalHosts))
	Log("Page of Hosts: "+str(PageOfHosts))

	while CreatePage:
		if int(PageOfHosts) != 0:
			if i < NumHostListing1:
				try:
					Host = Listing[i].xpath("./td/a/img")[0].get('title').split(' ')[0].split('.')[0].capitalize()
				except:
					Host = Listing[i].xpath("./td/a/img")[0].get('title').split(' ')[0].capitalize()
				MOVIE_PAGE = "http://" + MOVIE2K_URL + "/" + Listing[i].xpath("./td/a")[0].get('href')
				if type == 'TV Shows':
					DateAdded = dateadd
					Quality = "DVDRip/BDRip"
				else:
					DateAdded = Listing[i].xpath("./td/a")[0].text
					Quality = Listing[i].xpath("./td/img")[0].get('title').split(' ')[2]
				
				i += 1

			elif jj < NumHostListing2:
				ScriptListing = StringListing[k].text.split('links[')
				NumHosts = len(ScriptListing) - 2	
				try:
					Host = ScriptListing[sll].split('title=\\"')[1].split('\\"')[0].split(' ')[0].split('.')[0].capitalize()
				except:
					Host = ScriptListing[sll].split('title=\\"')[1].split('\\"')[0].split(' ')[0].capitalize()
				MOVIE_PAGE = "http://" + MOVIE2K_URL + "/" + ScriptListing[sll].split('href=\\"')[1].split('\\"')[0]
				if type == 'TV Shows':
					DateAdded = dateadd
					Quality = "DVDRip/BDRip"
				else:
					DateAdded = ScriptListing[sll].split('href=\\"')[1].split('\\">')[1].split(' <')[0]
					Quality = ScriptListing[sll].split('title=\\"')[2].split('\\"')[0].split(' ')[2]
				
				if sll == NumHosts:
					k += 1
					sll = 1
				else:
					sll += 1
				jj += 1
		else:
			CurrentPage = 0
			HostCount = 4
			DateAdded = dateadd
			MOVIE_PAGE = "http://" + MOVIE2K_URL + "/" + page
			if type == 'TV Shows':
				Quality = "DVDRip/BDRip"
			else:
				QualitySub = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')[1]
				Quality = QualitySub.xpath("./span/span/img")[0].get('title').split(' ')[2]

		if CurrentPage == int(PageOfHosts):
			if Host == 'N/a' or Host == 'Divx' or Host == 'DivX Hoster' or Host == 'Flash' or Host == 'Flash Hoster' or Host == 'Embed':
				Host = GetHost(Host=Host, url=MOVIE_PAGE)

			show = "ADDED: "+ DateAdded +" | HOST: "+ Host + " | QUALITY: " + Quality

			url = MOVIE_PAGE+"?title="+String.Quote(title, usePlus=True)+"&summary="+String.Quote(summary, usePlus=True)+"&show="+String.Quote(show, usePlus=True)+"&date="+String.Quote(str(date), usePlus=True)+"&thumb="+String.Quote(thumb, usePlus=True)+"&host="+Host+"&season="+str(season)+"&index="+str(index)+"&type="+String.Quote(type, usePlus=True)+"&genres="+String.Quote(genre, usePlus=True)+"&director="+String.Quote(director, usePlus=True)+"&actors="+String.Quote(actors, usePlus=True)+"&duration="+str(duration)+"&rating="+str(rating)+"&content_rating="+content_rating

			if Host == '180upload' or Host == 'Clicktoview' or Host == 'Vidbux' or Host == 'Vidplay' or Host == 'Vidxden':
				show_update = "Click here if you want OCR to try and decode Captcha text."
				oc.add(DirectoryObject(key=Callback(CaptchaSection, title=title, page=page, date=date, thumb=thumb, type=type, summary=summary, directors=directors, guest_stars=guest_stars, genres=genres, duration=duration, rating=rating, season=season, index=index, show=show_update, content_rating=content_rating, source_title=source_title, url=url, Host=Host), title=title, thumb=Callback(GetThumb, url=thumb), summary=show))
			else:
				if type == 'TV Shows':
					oc.add(EpisodeObject(
							url = url,
							title = title,
							summary = summary,
							directors = directors,
							guest_stars = guest_stars,
							#genres = genres,
							duration = duration,
							rating = rating,
							season = season,
							index = index,
							show = show,
							content_rating = content_rating,
							source_title = source_title,
							originally_available_at = date,
							thumb = Callback(GetThumb, url=thumb)))
				else:
					oc.add(MovieObject(
							url = url,
							title = title,
							summary = summary,
							directors = directors,
							genres = genres,
							duration = duration,
							rating = rating,
							content_rating = content_rating,
							source_title = show,
							originally_available_at = date,
							thumb = Callback(GetThumb, url=thumb)))

		if HostCount == 4:
			if CurrentPage == int(PageOfHosts):
				CreatePage = False
			CurrentPage += 1
			HostCount = 1
		else:
			HostCount += 1

		if HostCountTotal == TotalHosts:
			CreatePage = False
		else:
			HostCountTotal += 1

	if len(oc) < 1:
		oc = ObjectContainer(header="Sorry", message="This section does not contain any videos")

	return oc


#####################################################################################################
# This is the section for Host sites using Captcha
def CaptchaSection(title, page, date, thumb, type, summary, directors, guest_stars, genres, duration, rating, season, index, show, content_rating, source_title, url, Host):

	oc = ObjectContainer(title2=title)

	ICON_INSTRUCTIONS = "icon-instructions.png"
	INSTRUCTIONS_THUMB = R(ICON_INSTRUCTIONS)

	oc.add(DirectoryObject(key=Callback(RokuUsers, title="Special Instructions for Roku Users"), title="Special Instructions for Roku Users", thumb=INSTRUCTIONS_THUMB, summary="Click here to see special instructions necessary for Roku Users to input captcha text."))
	if type == 'TV Shows':
		oc.add(EpisodeObject(
				url = url,
				title = title,
				summary = summary,
				directors = directors,
				guest_stars = guest_stars,
				#genres = genres,
				duration = duration,
				rating = rating,
				season = season,
				index = index,
				show = show,
				content_rating = content_rating,
				source_title = source_title,
				originally_available_at = date,
				thumb = Callback(GetThumb, url=thumb)))
	else:
		oc.add(MovieObject(
				url = url,
				title = title,
				summary = summary,
				directors = directors,
				genres = genres,
				duration = duration,
				rating = rating,
				content_rating = content_rating,
				source_title = show,
				originally_available_at = date,
				thumb = Callback(GetThumb, url=thumb)))

	url = url.replace(Host,Host+"_2")
	hosts = LoadData(fp=CAPTCHA_DATA)
	Log(len(hosts))
	i = 1
	for gethost in hosts:
		if gethost[i]['host'] == Host:
			captchathumb = gethost[i]['thumb']
			GetUserAgent = gethost[i]['UserAgent']
			cookies = gethost[i]['captchacookies']
			HostPage = gethost[i]['HostPage']
			break
		else:
			i += 1

	oc.add(InputDirectoryObject(key=Callback(CaptchaInput, title=title, page=page, date=date, thumb=thumb, type=type, summary=summary, directors=directors, guest_stars=guest_stars, genres=genres, duration=duration, rating=rating, season=season, index=index, content_rating=content_rating, source_title=source_title, url=url, Host=Host), title=title, summary="Click here to use input screen for Captcha image.", thumb=Callback(GetThumb, url=captchathumb, HostPage=HostPage, GetUserAgent=GetUserAgent, cookies=cookies), prompt="Enter the text from the Captcha image."))

	return oc


#####################################################################################################
# This is captcha input for Roku users
def CaptchaInput(title, page, date, thumb, type, summary, directors, guest_stars, genres, duration, rating, season, index, content_rating, source_title, url, Host, query):

	oc = ObjectContainer(title2=title)

	show = "Host: " + Host + " - Captcha has been processed"
	hosts = LoadData(fp=CAPTCHA_DATA)

	i = 1
	for gethost in hosts:
		if gethost[i]['host'] == Host:
			gethost[i]['response'] = query
			break
		else:
			i += 1

	JsonWrite(fp=CAPTCHA_DATA, jsondata=hosts)

	if type == 'TV Shows':
		oc.add(EpisodeObject(
				url = url,
				title = title,
				summary = summary,
				directors = directors,
				guest_stars = guest_stars,
				#genres = genres,
				duration = duration,
				rating = rating,
				season = season,
				index = index,
				show = show,
				content_rating = content_rating,
				source_title = source_title,
				originally_available_at = date,
				thumb = Callback(GetThumb, url=thumb)))
	else:
		oc.add(MovieObject(
				url = url,
				title = title,
				summary = summary,
				directors = directors,
				genres = genres,
				duration = duration,
				rating = rating,
				content_rating = content_rating,
				source_title = show,
				originally_available_at = date,
				thumb = Callback(GetThumb, url=thumb)))

	return oc


#####################################################################################################
# This is special instructions for Roku users
def RokuUsers(title):

	return ObjectContainer(header="Special Instructions for Roku Users", message="To enter Captcha text, Roku users must be using version 2.6.6 of the Plex Roku Channel (currently the PlexTest channel). You can choose to type in the Captcha image text or allow the OCR to try and deocode it. However, the OCR decode rate is very low.  WARNING: DO NOT DIRECTLY TYPE OR PASTE THE TEXT IN THE INPUT CAPTCHA SECTION USING ROKU PLEX CHANNELS 2.6.4. THAT VERSION USES A SEARCH INSTEAD OF ENTRY SCREEN AND EVERY LETTER OF THE TEXT YOU ENTER WILL PRODUCE A SUBMIT FORM ON EACH CAPTCHA LETTER.")


####################################################################################################
def strip_one_space(s):

	if s.endswith(" "): s = s[:-1]
	if s.startswith(" "): s = s[1:]

	return s


####################################################################################################
def GetHost(Host, url):

	#
	#Check for Real Video Hoster if set to N/A or DivX Hoster or Flash Hoster is set
	#
	HostPageInfo = HTML.ElementFromURL(url)
	try:
		HostPage = HostPageInfo.xpath('//div[@id="maincontent5"]/div/iframe')[0].get('src')
	except:
		HostPage = HostPageInfo.xpath('//div[@id="maincontent5"]/div/a[@target="_blank"]')[0].get('href')
	Host = HostPage.split('http://')[1].split('.')[0].capitalize()
	if Host == 'Www' or Host == 'Embed':
		Host = HostPage.split('http://')[1].split('.')[1].capitalize()
	return Host


####################################################################################################
def GetLang(lang):
	if lang == "us_flag_small":
		r = "English"
	elif lang == "us_ger_small":
		r = "German"
	elif lang == "flag_japan":
		r = "Japanese"
	elif lang == "flag_spain":
		r = "Spanish"
	elif lang == "flag_turkey":
		r = "Turkish"
	elif lang == "flag_poland":
		r = "Polish"
	elif lang == "flag_greece":
		r = "Greek"
	elif lang == "flag_russia":
		r = "Russian"
	elif lang == "flag_india":
		r = "Hindi"
	elif lang == "flag_italy":
		r = "Italian"
	elif lang == "flag_france":
		r = "French"
	elif lang == "flag_netherlands":
		r = "Dutch"
	else:
		r = "N/A"

	return r


####################################################################################################
def GetThumb(url, HostPage=None, GetUserAgent=None, cookies={}):

	try:
		if GetUserAgent == None:
			imgData = HTTP.Request(url, cacheTime=CACHE_1HOUR).content
		else:
			headers = {}
			headers['Accept'] = 'image/png,image/*;q=0.8,*/*;q=0.5'
			headers['Connection'] = 'keep-alive'
			headers['Host'] = url.split('/')[2]
			headers['Referer'] = HostPage
			headers['User-Agent'] = GetUserAgent

			imgData = requests.get(url, headers=headers, cookies=cookies).content

		return DataObject(imgData, 'image/jpeg')
	except:
		return Redirect(R(ICON))


####################################################################################################
# This section is for Trailer Addict Search
####################################################################################################
@route(PREFIX + '/SearchTrailers')
def SearchTrailers(query):

	# Create a container to hold the results
	oc = ObjectContainer()

	url = 'http://www.traileraddict.com/search.php'
	website = 'http://www.traileraddict.com'
	params = {}
	cookies = {}
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'en-US,en;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Host': 'www.traileraddict.com',
		'Referer': 'http://www.traileraddict.com/',
		'User-Agent': UserAgent[UserAgentNum]
		}
	session = requests.session()

	s = session.get(website, headers=headers)
	for key, value in session.cookies.items():
			cookies[key] = value
	form = HTML.ElementFromString(s.content)

	for input in form.xpath('//form[@method="get"]/input'):
		if input.get('name') != None:
			key = input.get('name')
			value = input.get('value')
			params[key] = value
	params['q'] = query

	SEARCH_PAGE = requests.get(url, params=params, headers=headers, cookies=cookies)
	SEARCH_PAGE2 = SEARCH_PAGE.content.decode('cp1252').encode('utf-8')

	MovieTrailer = HTML.ElementFromString(SEARCH_PAGE2).xpath('//div[@class="leftcolumn"]/div')
	TotalTrailers = len(MovieTrailer) - 1
	i = 1
	while i < TotalTrailers:
		MOVIES_GET_THUMB = MovieTrailer[i].xpath('./div/center/div[@class="searchthumb"]')[0].get('style')
		try:
			MOVIES_THUMB = website + re.sub("\s", "", MOVIES_GET_THUMB.split('=')[1].split(')')[0])
		except:
			MOVIES_THUMB = website + MOVIES_GET_THUMB.split('url(')[1].split(')')[0]
		MOVIES_TITLE = MovieTrailer[i].xpath('./a')[0].text
		MOVIES_PAGE = website + MovieTrailer[i].xpath('./a')[0].get('href')
		MOVIES_DATE_RELEASE = MovieTrailer[i].xpath('./span')[0].text
		MOVIES_CONDENSED_CAST = MovieTrailer[i].text_content().split('Cast:')[1].split('Trailers')[0]
		MOVIES_SUMMARY = 'Release: ' + MOVIES_DATE_RELEASE + " | Cast: " + MOVIES_CONDENSED_CAST
		i += 1
		oc.add(DirectoryObject(key=Callback(TrailerResults, page=MOVIES_PAGE, title=MOVIES_TITLE, website=website), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))


	if len(oc) < 1:
		oc = ObjectContainer(header="Sorry", message="This Trailer Search did not contain any videos")

	return oc


####################################################################################################
@route(PREFIX + '/TrailerResults')
def TrailerResults(page, title, website):
	oc = ObjectContainer(title2=title)

	GetMovieTrailers = HTML.ElementFromURL(page)
			
	studio = re.sub("\s", " ", GetMovieTrailers.xpath('//div[@id="filmcontent"]/div')[2].text_content().split('Studio:')[1])
	writer = GetMovieTrailers.xpath('//div[@id="filmcontent"]/div')[5].text_content().split('Writer:')[1]
	cast = GetMovieTrailers.xpath('//div[@id="filmcontent"]/div')[6].text_content().split('Cast:')[1]
	director = re.sub("\s", " ", GetMovieTrailers.xpath('//div[@id="filmcontent"]/div')[4].text_content().split('Director: ')[1])
	genre = ''
	getgenres = GetMovieTrailers.xpath('//div[@id="filmcontent"]/div')[7]
	for aofgenres in getgenres.xpath('./a'):
		genre = genre + aofgenres.text + ','
	getrating = GetMovieTrailers.xpath('//div[@class="leftcolumn"]/center/div')[1]
	try:
		rating = getrating.xpath('./a/img')[0].get('src').split('front')[1].split('.')[0]
		if rating == 'na':
			rating = 0.0
	except:
		rating = 0.0
	date = GetMovieTrailers.xpath('//div[@id="filmcontent"]/div')[3].text_content().split('Release: ')[1]
	getthumb = GetMovieTrailers.xpath('//div[@id="filmcontent"]/div')[1]
	try:
	 	thumb = website + re.sub("\s", "", getthumb.xpath('./a/img')[0].get('src').split('=')[1].split('"')[0])
	except:
		thumb = website + getthumb.xpath('./img')[0].get('src')

	directors = []
	directors.append(director)
	genres = []
	genres = genre.split(',')
	content_rating = 'NR'
	show = 'Trailer Addict'
	Host = 'TrailerAddict'
	rating = float(rating)
	date = Datetime.ParseDate(date)
	type = 'Movies'
	season = 0
	index = 0
	actors = ','

	AllMovieTrailers = GetMovieTrailers.xpath('//div[@class="leftcolumn"]/div[@class="info"]')

	for Trailers in AllMovieTrailers:
		subtrailerurl = website + Trailers.xpath('./a')[0].get('href')
		TrailerText = Trailers.xpath('./div[@class="abstract"]')[0].text_content()
		TrailerDesc = TrailerText.split('Posted')[0]
		dateposted = re.sub("\s", " ", TrailerText.split('Posted ')[1].split('Tags:')[0])
		TrailerRuntime = TrailerText.split('Runtime: ')[1].split(' |')[0]
		duration = int((float(TrailerRuntime.split('m')[0])+float(TrailerRuntime.split('m')[1].split('s')[0])/60)*60*1000)
		trailertitle = Trailers.xpath('./div[@class="abstract"]/h2/a')[0].text

		summary = 'Posted: ' + dateposted + '| Studio: ' + studio + ' | Cast: ' + cast + ' | Desc: ' + TrailerDesc + ' | Writer: ' + writer

		url = subtrailerurl +"?title="+String.Quote(trailertitle, usePlus=True)+"&summary="+String.Quote(summary, usePlus=True)+"&show="+String.Quote(show, usePlus=True)+"&date="+String.Quote(str(date), usePlus=True)+"&thumb="+String.Quote(thumb, usePlus=True)+"&host="+Host+"&season="+str(season)+"&index="+str(index)+"&type="+String.Quote(type, usePlus=True)+"&genres="+String.Quote(genre, usePlus=True)+"&director="+String.Quote(director, usePlus=True)+"&actors="+String.Quote(actors, usePlus=True)+"&duration="+str(duration)+"&rating="+str(rating)+"&content_rating="+content_rating

		oc.add(MovieObject(
			url = url,
			title = trailertitle,
			summary = summary,
			directors = directors,
			genres = genres,
			duration = duration,
			rating = rating,
			content_rating = content_rating,
			source_title = show,
			originally_available_at = date,
			thumb = Callback(GetThumb, url=thumb)))
	return oc


####################################################################################################
# Set Up Tor Network Proxy
# This will be be used for Hosting sites that Block Countries - StreamCloud.eu & TheFile.me
# Or use it to hide your tracks...
####################################################################################################
def create_connection(address, timeout=None, source_address=None):
	sock = socks.socksocket()
	sock.connect(address)
	return sock


####################################################################################################
def connectTor():
	socks.usesystemdefaults()
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
	# patch the socket module
	socket.socket = socks.socksocket
	socket.create_connection = create_connection


####################################################################################################
def newIdentity(password):
	try:
		socks.setdefaultproxy()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("127.0.0.1", 9151))
		s.send('AUTHENTICATE "' + password + '"\r\n')
		response = s.recv(128)
		if response.startswith("250"):
			s.send("SIGNAL NEWNYM\r\n")
		else:
			Log("Error: Could not Change Tor IP - "+response)
		s.close()
		connectTor()
	except:
		Log("Error: Enable Tor Network Proxy - No connection could be made because the target machine actively refused it")


####################################################################################################
def EnableTorConnect():
	# Connect to Tor Proxy Network

	CheckProxy = Prefs['disabledTorProxy']
	ChangeIP = Prefs['disabledgetTorIP']
	CheckHash = Prefs['GenerateHashedPassword']
	password = Prefs['HashedControlPassword']

	if CheckProxy != 'Disabled':
		if CheckHash != 'Disabled':
			GenerateTorHashPassword(secret=password)
		if ChangeIP != 'Disabled':
			newIdentity(password=password)
		else:
			connectTor()
		try:
			conn = httplib.HTTPConnection("my-ip.heroku.com")
			conn.request("GET", "/")
			response = conn.getresponse()
			Log("MY Tor Proxy IP Address: " + response.read())
		except:
			Log("Error: Enable Tor Network Proxy - No connection could be made because the target machine actively refused it")


####################################################################################################
def GenerateTorHashPassword(secret):
	import os, binascii, hashlib
 
	#supply password
	#secret = 'foo'
 
	#static 'count' value later referenced as "c"
	indicator = chr(96)
 
	#used to generate salt
	rng = os.urandom
 
	#generate salt and append indicator value so that it
	salt = "%s%s" % (rng(8), indicator)
 
	#That's just the way it is. It's always prefixed with 16
	prefix = '16:'
 
	# swap variables just so I can make it look exactly like the RFC example
	c = ord(salt[8])
 
	# generate an even number that can be divided in subsequent sections. (Thanks Roman)
	EXPBIAS = 6
	count = (16+(c&15)) << ((c>>4) + EXPBIAS)
 
	d = hashlib.sha1()
 
	#take the salt and append the password
	tmp = salt[:8]+secret
 
	#hash the salty password as many times as the length of
	# the password divides into the count value
	slen = len(tmp)
	while count:
		if count > slen:
			d.update(tmp)
			count = count - slen
		else:
			d.update(tmp[:count])
			count = 0
	hashed = d.digest()
	#Convert to hex
	salt = binascii.b2a_hex(salt[:8]).upper()
	indicator = binascii.b2a_hex(indicator)
	torhash = binascii.b2a_hex(hashed).upper()
 
	#Put it all together into the proprietary Tor format.
	Log("Your Hashed Password and put this line in the torrc file: HashedControlPassword " + prefix + salt + indicator + torhash)