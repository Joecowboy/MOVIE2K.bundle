####################################################################################################
# Setting up imports

import os, sys
path = os.getcwd().split("?\\")[1].split('Plug-in Support')[0]+"Plug-ins\MOVIE2K.bundle\Contents\Services\URL\MOVIE2K\Modules"
sys.path.append(path)

import requests
import urllib
import re
import time
import socket
import httplib
import random

# Import SocksiPy
import sockschain as socks
def DEBUG(msg): Log(msg)
socks.DEBUG = DEBUG

# Random User Agent
UserAgent = ['Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Opera/9.25 (Windows NT 6.0; U; ja)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 2000) Opera 6.01 [ja]', 'Mozilla/5.0 (Windows; U; Windows NT 5.0; ja-JP; m18) Gecko/20010131 Netscape6/6.01', 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/85.7 (KHTML, like Gecko) Safari/85.7']
UserAgentNum = random.randrange(0, len(UserAgent)-1, 1)

PREFIX         = "/video/movie2k"
NAME           = "Movie2k"
ART            = "art-default.jpg"
ICON           = "icon-default.png"
MOVIE2K_URL    = Prefs['movie2k_url']


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

	HTTP.CacheTime = 0
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
	cookiejar = {"xxx2": "ok", "domain": ".movie4k.to", "path": "/", "onlylanguage": "deleted", "lang": "en"}
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
	oc = ObjectContainer(title2="Search Results", view_group="InfoList")
	
	#AutoComplete = "http://" + MOVIE2K_URL + "/searchAutoCompleteNew.php?search=" + urllib.quote_plus(query)
	#AutoSearch = HTML.ElementFromURL(AutoComplete).xpath('//table/tr')

	#for SearchList in AutoSearch:
	#	MOVIES_TITLE = SearchList.xpath('./td/a')[0].text
		
	type = 'N/A'
	dateadd = 'N/A'
	ads = 'ads.affbuzzads.com'
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
		try:
			if ads == MOVIES_PAGE.split('/')[2]:
				Log("Bad search results")
				oc = MessageContainer("Search Error", "Search did not return any positive results.  Please try another key word search!")
		except:
			if MOVIES_LANG == GetLanguage() or MOVIES_LANG == 'N/A' or GetLanguage() == 'All':
				oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		i += 1

	return oc


####################################################################################################
@route(PREFIX + '/MyMovie2k')
def MyMovie2k(title):

	# Attempt to login
	loginResult = Movie2kLogin()
	Log("My Movie2k Login success: " + str(loginResult))

	ICON_MYUPLOADS = "icon-myuploads.png"
	MYUPLOADS_THUMB = R(ICON_MYUPLOADS)
	ICON_MYMESSAGES = "icon-mymessages.png"
	MYMESSAGES_THUMB = R(ICON_MYMESSAGES)

	if loginResult:
		oc = ObjectContainer(title2=title)
		oc.add(DirectoryObject(key = Callback(Queue, title="My Uploads"), title="My Uploads", summary="Show all online, offline, waiting and queued links!", thumb=MYUPLOADS_THUMB))
		oc.add(DirectoryObject(key = Callback(Messages, title="My Messages"), title = "My Messages", summary="Show messages from your Inbox!", thumb=MYMESSAGES_THUMB))
	else:
		oc = MessageContainer("User info required", "Please enter your Movie2k username and password in Preferences.")

	return oc


####################################################################################################
@route(PREFIX + '/Queue')
def Queue(title):
	
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
		Host = Movies[i].xpath('./td')[1].text_content()
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

	return oc


####################################################################################################
@route(PREFIX + '/Messages')
def Messages(title):
	
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

	#Add Genre Pages to TV Page
	GENRE_PAGE = "http://" + MOVIE2K_URL + "/genres-tvshows.html"
	
	NotSkip = True

	for Genre in HTML.ElementFromURL(GENRE_PAGE).xpath('//div[@id="content"]/table[@id="tablemovies"]/tr'):
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
		TVSHOW_YEAR = re.sub('[^0-9]', '', TVSHOWS_DIV[i].xpath('./div[@class="beschreibung"]/span')[0].text_content().split('| : ')[1])
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
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/index.php?lang=us"
		oc.add(DirectoryObject(key=Callback(CinemaMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		#Add Latest Updates Movie Page
		MOVIES_TITLE = "Newly Added Movies"
		MOVIES_SUMMARY = "Your Latest Updates to the Movies database!"
		MOVIES_THUMB = R(ICON_UPDATES)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/movies-updates"
		oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		#Add Genre Pages to Movie Page
		GENRE_PAGE = "http://" + MOVIE2K_URL + "/genres-movies.html"

	elif type == 'XXX Movies':
		#Add Latest Updates XXX Movie Page
		PORN_TITLE = "Newly Added XXX Movies"
		PORN_SUMMARY = "Your Latest Updates to the XXX Movies database!"
		PORN_THUMB = R(ICON_UPDATES)
		PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-updates"
		oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, genre=Genre_Type, type=type), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

		#Add Genre Pages to XXX Movies Page
		GENRE_PAGE = "http://" + MOVIE2K_URL + "/genres-xxx.html"
	
	NotSkip = True
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(GENRE_PAGE, headers=headers, cookies=cookies)

	for Genre in HTML.ElementFromString(req.content).xpath('//div[@id="content"]/table[@id="tablemovies"]/tr'):
		Genre_Type = Genre.xpath('./td[@id="tdmovies"]/a')[0].text
		ICON_MOVIES = "icon-"+Genre_Type.lower()+".png"
		MOVIES_TITLE = Genre_Type+" "+type
		MOVIES_SUMMARY = "Your "+Genre_Type+" Movie database!"
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
			try:
				MOVIES_TD = Movie.xpath('./div')[0]
			except:
				MOVIES_TD = Movie
			MOVIES_TITLE = MOVIES_TD.xpath("./a/img")[0].get('title').replace(' kostenlos','')
			MOVIES_PAGE = MOVIES_TD.xpath("./a")[0].get('href')
			MOVIES_THUMB = MOVIES_TD.xpath("./a/img")[0].get('src')
			MOVIES_YEAR = time.strftime("%Y", time.localtime(time.time()))
			MOVIES_LANG = "English"
			MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the Cinema Movies line up on Movie2k."

			oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		except:
			pass

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

	oc = ObjectContainer(title2=title, view_group="InfoList")

	MOVIE_PAGE_HTML = HTML.ElementFromURL("http://"+MOVIE2K_URL+"/"+page)

	GET_THUMB = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')[0]
	thumb = GET_THUMB.xpath('./a/img')[0].get('src')

	if thumb.split('/')[4] == "noposter.gif":
		if thumbck != "" and thumbck != None:
			thumb = thumbck

	NumHostListing1 = len(MOVIE_PAGE_HTML.xpath('//div[@id="menu"]//tr[@id="tablemoviesindex2"]'))
	StringListing = MOVIE_PAGE_HTML.xpath('//div[@id="menu"]//script[@type="text/javascript"]')
	NumStringListing = len(StringListing)
	NumHostListing2 = 0
	nsl = 0
	i = 1

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
		MOVIES_SUMMARY = "Page - " + str(i) + " of hosting sites."
		oc.add(DirectoryObject(key=Callback(TheMovieListings, title=title, page=page, date=date, dateadd=dateadd, thumb=thumb, type=type, PageOfHosts=i), title=title, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=thumb)))
		i += 1

	return oc


####################################################################################################
@route(PREFIX + '/TVandTheMovieListings')
def TheMovieListings(title, page, date, dateadd, thumb, type, PageOfHosts, Host=None):

	oc = ObjectContainer(title2=title, view_group="InfoList")

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
			try:
				date = re.sub("\s", "", MOVIE_INFO.split('Land/Year: ')[1].split('/')[1].split(' ')[0])
				if date == "N/A":
					date =  "0001"
				else:
					try:
						tempdate = int(date)
					except:
						date = re.sub("\s", "", MOVIE_INFO.split('Land/Year: ')[1].split(' ')[0])
						if date == "N/A":
							date =  "0001"
						else:
							try:
								tempdate = int(date)
							except:
								date = re.sub("\s", "", MOVIE_INFO.split('Land/Year: ')[1].split(' ')[1])
			except:
				date = re.sub("\s", "", MOVIE_INFO.split('Land/Jahr: ')[1].split(' ')[0])
				if date == "N/A":
					date = "0001"
				else:
					try:
						tempdate = int(date)
					except:
						try:
							date = re.sub("\s", "", MOVIE_INFO.split('Land/Jahr: ')[1].split('/')[1].split(' ')[0])
						except:
							date = MOVIE_INFO.split('Land/Jahr: ')[1].split(' ')[1]
		except:
			date = "0001"

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
			if Host == 'N/a' or Host == 'Divx' or Host == 'Flash':
				Host = GetHost(Host=Host, url=MOVIE_PAGE)

			show = "ADDED: "+ DateAdded +" | HOST: "+ Host + " | QUALITY: " + Quality

			url = MOVIE_PAGE+"?title="+String.Quote(title, usePlus=True)+"&summary="+String.Quote(summary, usePlus=True)+"&show="+String.Quote(show, usePlus=True)+"&date="+String.Quote(str(date), usePlus=True)+"&thumb="+String.Quote(thumb, usePlus=True)+"&host="+Host+"&season="+str(season)+"&index="+str(index)+"&type="+String.Quote(type, usePlus=True)+"&genres="+String.Quote(genre, usePlus=True)+"&director="+String.Quote(director, usePlus=True)+"&actors="+String.Quote(actors, usePlus=True)+"&duration="+str(duration)+"&rating="+str(rating)+"&content_rating="+content_rating

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


####################################################################################################
def StripArray(arraystrings):

	temparraystring = []
	
	for array_elem in arraystrings:
		elem = re.sub("[\n\t\xa0]", "", array_elem).strip()
		temparraystring.append(elem)

	return temparraystring


####################################################################################################
def GetHost(Host, url):

	#
	#Check for Real Video Hoster if set to N/A or DivX Hoster or Flash Hoster is set
	#
	HostPageInfo = HTML.ElementFromURL(url)
	try:
		HostPage = HostPageInfo.xpath('//div[@id="emptydiv"]/iframe')[0].get('src')
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
def GetThumb(url):

	try:
		data = HTTP.Request(url, cacheTime=CACHE_1MONTH).content
		return DataObject(data, 'image/jpeg')
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