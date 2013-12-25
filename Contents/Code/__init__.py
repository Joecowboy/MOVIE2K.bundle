####################################################################################################
# Setting up imports

import os, sys
try:
	path = os.getcwd().split("?\\")[1].split('Plug-in Support')[0]+"Plug-ins\MOVIE2K.bundle\Contents\Services\URL\MOVIE2K\Modules"
	DownloadPath = '\\'
except:
	path = os.getcwd().split("Plug-in Support")[0]+"Plug-ins/MOVIE2K.bundle/Contents/Services/URL/MOVIE2K/Modules"
	DownloadPath = '/'
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
import subprocess
import HostServices
import HostSites
import HostVideoDownload

# Import SocksiPy
import sockschain as socks
socks.DEBUG = Log

from HostServices import StripArray
from HostServices import LoadData
from HostServices import JsonWrite
from HostServices import CookieDict
from HostServices import GetHostPageURL
from HostVideoDownload import GetHostVideo
from HostVideoDownload import CheckForDownload
from HostVideoDownload import KillMyDownloadThread
from HostVideoDownload import ResumeMyDownload
from HostVideoDownload import combine_files

# Random User Agent
UserAgent = ['Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Opera/9.25 (Windows NT 6.0; U; ja)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 2000) Opera 6.01 [ja]', 'Mozilla/5.0 (Windows; U; Windows NT 5.0; ja-JP; m18) Gecko/20010131 Netscape6/6.01', 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/85.7 (KHTML, like Gecko) Safari/85.7']
UserAgentNum = random.randrange(0, len(UserAgent)-1, 1)

# Movie2k Plugin Version
Version = Prefs['version']

# If Video Error Enabled or Disabled
VideoError = Prefs["videoerror"]

# Set up Host Services
HostServices.R              = R
HostServices.Log            = Log
HostServices.HTML           = HTML
HostServices.String         = String
HostServices.Version        = Version
HostServices.VideoError     = VideoError
HostServices.UserAgent      = UserAgent[UserAgentNum]
HostSites.Log               = Log
HostSites.XML               = XML
HostSites.HTML              = HTML
HostSites.String            = String
HostSites.Version           = Version
HostSites.UserAgent         = UserAgent[UserAgentNum]
HostVideoDownload.Log       = Log
HostVideoDownload.String    = String
HostVideoDownload.UserAgent = UserAgent[UserAgentNum]

PREFIX            = "/video/movie2k"
NAME              = "Movie2k"
ART               = "art-default.jpg"
ICON              = "icon-default.png"
CAPTCHA_DATA      = "captcha.data.json"
FAVORITES_DATA    = "favorites.data.json"
WATCHIT_DATA      = "watchit.data.json"
PROXIFIER_PROCESS = None
GoodLink          = None


####################################################################################################
def Start():

	# Initialize the plug-in
	#Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

	# Setup the default attributes for the ObjectContainer
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	#ObjectContainer.view_group = "InfoList"


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

	oc = ObjectContainer()

	# Enable Tor Proxy
	EnableTorConnect()

	# Clean Up Any Failed File Deletions of Video Downloads
	CheckFailedFileDeletions()

	#Add Movie4k.to site
	ICON_MOVIES4k_TO  = "icon-movie4k-to.png"
	MOVIES_TITLE = "Movie4k.to"
	MOVIES_SUMMARY = "Your Movies, Blockbuster and TV Shows database!"
	MOVIES_THUMB = R(ICON_MOVIES4k_TO)
	if Prefs['proxy_movie2k_url'] != "Disabled":
		if Prefs['proxy_movie2k_url'] != "91.202.62.123":
			MOVIE2K_URL = Prefs['proxy_movie2k_url']
	else:
		MOVIE2K_URL = "www.movie4k.to"
	oc.add(DirectoryObject(key=Callback(SubMainMenu, title=MOVIES_TITLE, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	#Add Movie2k.tv site
	ICON_MOVIES2k_TV  = "icon-movie2k-tv.png"
	MOVIES_TITLE = "Movie2k.tv"
	MOVIES_SUMMARY = "Your Movies, Blockbuster and TV Shows database!"
	MOVIES_THUMB = R(ICON_MOVIES2k_TV)
	if Prefs['proxy_movie2k_url'] != "Disabled":
		if Prefs['proxy_movie2k_url'] == "91.202.62.123":
			Prefs['proxy_movie2k_url'] = MOVIE2K_PROXY_URL
	else:
		MOVIE2K_URL = "www.movie2k.tv"
	oc.add(DirectoryObject(key=Callback(SubMainMenu, title=MOVIES_TITLE, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	#Add Movie2k.sx site
	ICON_MOVIES2k_SX  = "icon-movie2k-sx.png"
	MOVIES_TITLE = "Movie2k.sx"
	MOVIES_SUMMARY = "Your Movies, Blockbuster and TV Shows database!"
	MOVIES_THUMB = R(ICON_MOVIES2k_SX)
	MOVIE2K_URL = "www.movie2k.sx"
	oc.add(DirectoryObject(key=Callback(SubMainMenu, title=MOVIES_TITLE, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	#Add Movie2k.tl site
	ICON_MOVIES2k_TL  = "icon-movie2k-tl.png"
	MOVIES_TITLE = "Movie2k.tl"
	MOVIES_SUMMARY = "Your German Movies, Blockbuster and TV Shows database!"
	MOVIES_THUMB = R(ICON_MOVIES2k_TL)
	MOVIE2K_URL = "www.movie2k.tl"
	oc.add(DirectoryObject(key=Callback(SubMainMenu, title=MOVIES_TITLE, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	#Add Search only for Plex/Web
	if Client.Product == "Web Client":
		ICON_SEARCH = "icon-search.png"
		title = "Movie2k Search"
		SEARCH_TITLE = "Search the "+title+" Database"
		SEARCH_SUMMARY ="Find a TV Show or Movie from the "+title+" database!"
		SEARCH_THUMB = R(ICON_SEARCH)
		MOVIE2K_URL = Prefs['movie2k_url']
		oc.add(InputDirectoryObject(key=Callback(Search, title=title, MOVIE2K_URL=MOVIE2K_URL), title=SEARCH_TITLE, summary=SEARCH_SUMMARY, prompt="Search for", thumb=SEARCH_THUMB))

	#Add Movie2k Plugin Setup
	ICON_PREFS = "icon-preferences.png"
	PREFS_TITLE = "Preferences"
	PREFS_SUMMARY = "Update login and channel information!"
	PREFS_THUMB = R(ICON_PREFS)
	oc.add(PrefsObject(title=PREFS_TITLE, summary=PREFS_SUMMARY, thumb=PREFS_THUMB))

	return oc


###################################################################################################
@route(PREFIX + '/SubMainMenu')
def SubMainMenu(title, MOVIE2K_URL):

	# INitialize My Movie2k Login
	loginResult = Movie2kLogin(MOVIE2K_URL=MOVIE2K_URL)
	Log("Login success: " + str(loginResult))

	oc = ObjectContainer()

	#Add Movie Links
	ICON_MOVIES  = "icon-movies.png"
	MOVIES_TITLE = "Movies"
	MOVIES_SUMMARY = "Your Movie and Blockbuster database!"
	MOVIES_THUMB = R(ICON_MOVIES)
	oc.add(DirectoryObject(key=Callback(Movies, title=MOVIES_TITLE, type='Movies', MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	#Add TV Show Links
	ICON_TVSHOWS = "icon-tvshows.png"
	TV_SHOWS_TITLE = "TV Shows"
	TV_SHOWS_SUMMARY = "Your TV Shows database!"
	TV_SHOWS_THUMB = R(ICON_TVSHOWS)
	oc.add(DirectoryObject(key=Callback(TVShows, title=TV_SHOWS_TITLE, type='TV Shows', MOVIE2K_URL=MOVIE2K_URL), title=TV_SHOWS_TITLE, summary=TV_SHOWS_SUMMARY, thumb=TV_SHOWS_THUMB))

	#Add Adult Movie Links
	ICON_MOVIES  = "icon-xxx movies.png"
	XXXMOVIES_TITLE = "XXX Movies"
	XXXMOVIES_SUMMARY = "Your XXX Movies database!"
	XXXMOVIES_THUMB = R(ICON_MOVIES)
	if DisableAdult():
		oc.add(DirectoryObject(key=Callback(Movies, title=XXXMOVIES_TITLE, type='XXX Movies', MOVIE2K_URL=MOVIE2K_URL), title=XXXMOVIES_TITLE, summary=XXXMOVIES_SUMMARY, thumb=XXXMOVIES_THUMB))

	#Add Movie4k Added Links and Inbox
	ICON_MYMOVIE2k = "icon-mymovie2k.png"
	MYMOVIE2K_TITLE = "My Movie2k"
	MYMOVIE2K_SUMMARY = "My Uploads and Inbox on "+title+", My Favorites and My Watchit Later!"
	MYMOVIE2K_THUMB = R(ICON_MYMOVIE2k)
	oc.add(DirectoryObject(key = Callback(MyMovie2k, title=MYMOVIE2K_TITLE, MOVIE2K_URL=MOVIE2K_URL), title=MYMOVIE2K_TITLE, summary=MYMOVIE2K_SUMMARY, thumb=MYMOVIE2K_THUMB))

	#Add Search Links
	ICON_SEARCH = "icon-search.png"
	SEARCH_TITLE = "Search the "+title+" Database"
	SEARCH_SUMMARY ="Find a TV Show or Movie from the "+title+" database!"
	SEARCH_THUMB = R(ICON_SEARCH)
	oc.add(InputDirectoryObject(key=Callback(Search, title=title, MOVIE2K_URL=MOVIE2K_URL), title=SEARCH_TITLE, summary=SEARCH_SUMMARY, prompt="Search for", thumb=SEARCH_THUMB))
	#oc.add(SearchDirectoryObject(identifier="com.plexapp.plugins.movie2k", title=TRAILERSEARCH_TITLE, prompt=TRAILERSEARCH_SUMMARY, thumb=TRAILERSEARCH_THUMB))

	#Add Trailer Search Links
	ICON_TRAILERSEARCH = "icon-trailer-addict.png"
	TRAILERSEARCH_TITLE = "Search for Your Daily Dose of Hi-Res Movie Trailers"
	TRAILERSEARCH_SUMMARY ="Find a Movie Trailer from the Trailer Addict database!"
	TRAILERSEARCH_THUMB = R(ICON_TRAILERSEARCH)
	oc.add(InputDirectoryObject(key=Callback(SearchTrailers), title=TRAILERSEARCH_TITLE, summary=TRAILERSEARCH_SUMMARY, prompt="Search for", thumb=TRAILERSEARCH_THUMB))

	return oc


####################################################################################################  
def Movie2kLogin(MOVIE2K_URL):

	username = Prefs["username"]
	password = Prefs["password"]
	cookiejar = {"xxx2": "ok", "xxx": "ok", "onlylanguage": "", "lang": "en"}
	Dict['_movie2k_uid'] = cookiejar
	HTTP.Headers['Cookie'] = cookiejar

	if (username != None) and (password != None):
		try:
			files = {}
			cookies = {}
			session = requests.session()
			url = "http://" + MOVIE2K_URL + "/login.php?ua=login"
			if MOVIE2K_URL == "www.movie2k.tl":
				authentication_values = {"login_username": username, "login_pass": password}
			else:
				authentication_values = {"username": username, "password": password}
			authentication_headers = {"Host": MOVIE2K_URL, "Referer": url, "User-Agent": UserAgent[UserAgentNum]}
			req = session.post(url, data=authentication_values, headers=authentication_headers, files=files, allow_redirects=True)
			if MOVIE2K_URL == "www.movie2k.tl":
				try:
					data = HTML.ElementFromString(req.content).xpath('//div[@id="maincontent4"]/p')[0].text
				except:
					data = "Logged in!"
			else:
				data = req.content.split('<div id="maincontent4">')[1].split('<STRONG>')[1].split('</STRONG>')[0]

			if data == "Logged in!":
				cookies = CookieDict(cookies=session.cookies)
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
def Search(title, MOVIE2K_URL, query):

	#Search movie4k.to for movies using user input, and populate a list with the results

	# Create a container to hold the results
	oc = ObjectContainer(title2="Search Results")
	
	#AutoComplete = "http://" + MOVIE2K_URL + "/searchAutoCompleteNew.php?search=" + urllib.quote_plus(query)
	#AutoSearch = HTML.ElementFromURL(AutoComplete).xpath('//table/tr')

	#for SearchList in AutoSearch:
	#	MOVIES_TITLE = SearchList.xpath('./td/a')[0].text

	type = 'Movies'
	dateadd = 'N/A'
	if MOVIE2K_URL == "www.movie2k.tl":
		url = 'http://www.movie2k.tl/search'
		payload = {'searchquery': query}
		elm1 = 'body'
		elm2 = '//table[@id="tablemoviesindex"]/tbody/tr'
	elif MOVIE2K_URL == "www.movie2k.sx":
		url = 'http://www.movie2k.sx/search'
		payload = {'q': query}
		elm1 = '//table[@id="tablemoviesindex"]'
		elm2 = '//table[@id="tablemoviesindex"]/tr'
	else:
		url = 'http://' + MOVIE2K_URL + '/movies.php?list=search'
		payload = {'search': query}
		elm1 = 'div[@id="maincontent4"]'
		elm2 = '//table[@id="tablemoviesindex"]/tr'

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
		'Referer': url,
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': UserAgent[UserAgentNum]
		}

	if MOVIE2K_URL == "www.movie2k.sx":
		SEARCH_PAGE = requests.get(url, data=payload, headers=headers, allow_redirects=True, cookies=cookies)
	else:
		SEARCH_PAGE = requests.post(url, data=payload, headers=headers, allow_redirects=True, cookies=cookies)

	try:
		GET_THUMB = HTML.ElementFromString(SEARCH_PAGE.content).xpath('//'+elm1+'/script')
	except:
		GET_THUMB = None

	Movie = HTML.ElementFromString(SEARCH_PAGE.content).xpath(elm2)

	i = 0
	while (i < len(Movie)):
		MOVIES_TD = Movie[i].xpath('./td[@id="tdmovies"]')
		MOVIES_TITLE = re.sub('\t\r\0', '', MOVIES_TD[0].xpath(u'./a')[0].text).replace('     ', '').strip()

		try:
			try:
				MOVIES_YEAR = MOVIES_TD[1].xpath('./div')[7].text
			except:
				MOVIES_YEAR = MOVIES_TD[2].text.strip()
			if MOVIES_YEAR == None or MOVIES_YEAR == "":
				MOVIES_YEAR = "N/A"
		except:
			MOVIES_YEAR = "N/A"

		try:
			try:
				LANGUAGE_URL = MOVIES_TD[4].xpath('./img')[0].get('src')
			except:
				LANGUAGE_URL = MOVIES_TD[5].xpath('./img')[0].get('src')
			try:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
			except:
				MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
		except:
			if MOVIE2K_URL == "www.movie2k.sx":
				MOVIES_LANG = MOVIES_TD[3].text
				if MOVIES_LANG == None or MOVIES_LANG == "":
					MOVIES_LANG = "N/A"
				else:
					MOVIES_LANG = MOVIES_LANG.capitalize()
			else:
				MOVIES_LANG = "N/A"

		MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the search line up on "+title+"."
		MOVIES_PAGE = MOVIES_TD[0].xpath('./a')[0].get('href')

		try:
			if MOVIE2K_URL == "www.movie2k.sx":
				jj = i
				SiteURL = "http://www.movie2k.sx"
			else:
				jj = 0
				SiteURL = ""
			MOVIES_THUMB = SiteURL + GET_THUMB[jj].text.split(Movie[i].get('id'))[1].split("img src='")[1].split("'")[0]
		except:
			MOVIES_THUMB = None

		MOVIES_HOST = re.sub(r'[^a-zA-Z0-9:!]', '', MOVIES_TD[1].text_content())

		if MOVIES_HOST == "downloadnow!":
			oc = MessageContainer("Search Error", "Search did not return any positive results.  Please try another key word search!")
		elif MOVIES_LANG == GetLanguage() or MOVIES_LANG == 'N/A' or GetLanguage() == 'All':
			if "seri" in MOVIES_PAGE or "tvshow" in MOVIES_PAGE:
				if MOVIES_THUMB == None:
					MOVIES_THUMB = "N/A"
				oc.add(DirectoryObject(key=Callback(TVShowSeasons, title=MOVIES_TITLE, page=MOVIES_PAGE, genre="N/A", type="TV Shows", MOVIE2K_URL=MOVIE2K_URL, thumb=MOVIES_THUMB, MOVIES_LANG=MOVIES_LANG), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
			else:
				oc.add(DirectoryObject(key=Callback(SubGroupMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type, summary=MOVIES_SUMMARY, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		i += 1

	if len(oc) < 1:
		oc = MessageContainer("Search Error", "Search did not return any positive results.  Please try another key word search!")

	return oc


####################################################################################################
@route(PREFIX + '/MyMovie2k')
def MyMovie2k(title, MOVIE2K_URL):

	oc = ObjectContainer(title2=title)

	# My Movie2k
	ICON_MYMOVIE2k = "icon-mymovie2k.png"
	MYMOVIE2K_THUMB = R(ICON_MYMOVIE2k)
	title = "My Movie2k"
	WhichSection = "MyMovie2k"
	summary = "List My Uploads and Inbox on "+MOVIE2K_URL.split('www.')[1].capitalize()+"!"
	oc.add(DirectoryObject(key = Callback(SubMyMovie2k, title=title, MOVIE2K_URL=MOVIE2K_URL, WhichSection=WhichSection), title=title, summary=summary, thumb=MYMOVIE2K_THUMB))

	# My Favorite Movie4k.to links
	ICON_MYFAVORITES = "icon-my-favorites.png"
	MYFAVORITES_THUMB = R(ICON_MYFAVORITES)
	title = "My Favorite Links"
	summary = "Show my favorite links from Movie4k.to, Movie2k.tv, Movie2k.sx and Movie2k.tl!"
	WhichSection = "MyFavorites"
	oc.add(DirectoryObject(key = Callback(SubMyMovie2k, title=title, MOVIE2K_URL=MOVIE2K_URL, WhichSection=WhichSection), title=title, summary=summary, thumb=MYFAVORITES_THUMB))

	#Add My Watchit Later Videos
	ICON_MYWATCHITLATER  = "icon-my-watchit-later.png"
	MYWATCHITLATER_THUMB = R(ICON_MYWATCHITLATER)
	title = "My Watchit Later Videos"
	summary = "Playback Local Downloads from Movie2k Blockbuster and TV Shows database!"
	WhichSection = "MyWatchitLater"
	oc.add(DirectoryObject(key = Callback(SubMyMovie2k, title=title, MOVIE2K_URL=MOVIE2K_URL, WhichSection=WhichSection), title=title, summary=summary, thumb=MYWATCHITLATER_THUMB))

	return oc

####################################################################################################
@route(PREFIX + '/SubMyMovie2k')
def SubMyMovie2k(title, MOVIE2K_URL, WhichSection):

	oc = ObjectContainer(title2=title)
	
	if WhichSection == "MyMovie2k":
		# Attempt to login
		loginResult = Movie2kLogin(MOVIE2K_URL=MOVIE2K_URL)
		Log("My Movie2k Login success: " + str(loginResult))

		# My Uploads on Movie4k.to
		ICON_MYUPLOADS = "icon-myuploads.png"
		MYUPLOADS_THUMB = R(ICON_MYUPLOADS)
		title = "My Uploads"
		summary = "Show all online, offline, waiting and queued links on "+MOVIE2K_URL.split('www.')[1].capitalize()+"!"
		oc.add(DirectoryObject(key = Callback(Queue, title=title, loginResult=loginResult, MOVIE2K_URL=MOVIE2K_URL), title=title, summary=summary, thumb=MYUPLOADS_THUMB))

		# My Messages on Movie4k.to
		ICON_MYMESSAGES = "icon-mymessages.png"
		MYMESSAGES_THUMB = R(ICON_MYMESSAGES)
		title = "My Messages"
		summary = "Show messages from your Inbox on "+MOVIE2K_URL.split('www.')[1].capitalize()+"!"
		oc.add(DirectoryObject(key = Callback(Messages, title=title, loginResult=loginResult, MOVIE2K_URL=MOVIE2K_URL), title=title, summary=summary, thumb=MYMESSAGES_THUMB))

	elif WhichSection == "MyFavorites":
		# User input instructions
		ICON_INSTRUCTIONS = "icon-instructions.png"
		INSTRUCTIONS_THUMB = R(ICON_INSTRUCTIONS)
		title = "Special Instructions for Roku Users"
		summary = "Click here to see special instructions necessary for Roku Users for Add Favorite."
		oc.add(DirectoryObject(key=Callback(RokuUsersMyFavorites, title=title), title=title, summary=summary, thumb=INSTRUCTIONS_THUMB))

		# My Favorite Movie4k.to links
		ICON_MYFAVORITES = "icon-my-favorites.png"
		MYFAVORITES_THUMB = R(ICON_MYFAVORITES)
		title = "My Favorite Links"
		summary = "Show my favorite links from Movie4k.to, Movie2k.tv, Movie2k.sx and Movie2k.tl!"
		oc.add(DirectoryObject(key = Callback(MyFavoriteURL, title=title, MOVIE2K_URL=MOVIE2K_URL), title=title, summary=summary, thumb=MYFAVORITES_THUMB))

		# Add Favorite Movie4k.to link
		ICON_ADDFAVORITE = "icon-add-favorite.png"
		ADDFAVORITE_THUMB = R(ICON_ADDFAVORITE)
		title = "Add Favorite Link"
		summary = "Add a favorite link from Movie4k.to, Movie2k.tv, Movie2k.sx and Movie2k.tl!"
		prompt = "Add a favorite link from Movie2k!"
		oc.add(InputDirectoryObject(key=Callback(InputFavoriteURL, title=title, MOVIE2K_URL=MOVIE2K_URL), title=title, summary=summary, thumb=ADDFAVORITE_THUMB, prompt=prompt))

		# Delete Favorite Movie4k.to link
		ICON_DELETEFAVORITE = "icon-delete-favorite.png"
		DELETEFAVORITE_THUMB = R(ICON_DELETEFAVORITE)
		title = "Delete Favorite Links"
		summary = "Delete my favorite links from Movie2k!"
		oc.add(DirectoryObject(key = Callback(DeleteFavoriteURL, title=title), title=title, summary=summary, thumb=DELETEFAVORITE_THUMB))

	elif WhichSection == "MyWatchitLater":
		#Add My Watchit Later Videos
		ICON_MYWATCHITLATER  = "icon-my-watchit-later.png"
		MYWATCHITLATER_THUMB = R(ICON_MYWATCHITLATER)
		title = "My Watchit Later Videos"
		summary = "Playback Local Downloads from Movie2k Blockbuster and TV Shows database!"
		oc.add(DirectoryObject(key=Callback(PlaybackDownloads, title=title), title=title, summary=summary, thumb=MYWATCHITLATER_THUMB))

		# Delete Watchit Later Videos
		ICON_DELETEWATCHITLATER = "icon-delete-videos.png"
		DELETEWATCHITLATER_THUMB = R(ICON_DELETEWATCHITLATER)
		title = "Delete Watchit Later Videos"
		summary = "Delete my wathit later videos from Movie2k Hosts!"
		oc.add(DirectoryObject(key = Callback(DeleteWatchitLaterVideo, title=title), title=title, summary=summary, thumb=DELETEWATCHITLATER_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/RokuUsersMyFavorites')
def RokuUsersMyFavorites(title):

	return ObjectContainer(header="Special Instructions for Roku Users", message="Inputting Movie4k URL, Roku users must be using version 2.6.7 or later of the Plex Roku Channel. If you do not want to input the Movie4k URL via the Roku input screen you can use the online Rokue remote control.  It can be found at:  http://www.remoku.tv   WARNING: DO NOT DIRECTLY TYPE OR PASTE THE TEXT IN THE INPUT CAPTCHA SECTION USING ROKU PLEX CHANNELS 2.6.4. THAT VERSION USES A SEARCH INSTEAD OF ENTRY SCREEN AND EVERY LETTER OF THE TEXT YOU ENTER WILL PRODUCE A SUBMIT FORM ON EACH LETTER.")


####################################################################################################
@route(PREFIX + '/MyFavoriteURL')
def MyFavoriteURL(title, MOVIE2K_URL):

	oc = ObjectContainer(title2=title)

	hosts = LoadData(fp=FAVORITES_DATA, GetJson=2)
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
			oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
	
	if len(oc) < 1:
		oc = ObjectContainer(header="We Apologize", message="This section does not contain any My Favorite videos.  Please add a video to view.")

	return oc

####################################################################################################
@route(PREFIX + '/InputFavoriteURL')
def InputFavoriteURL(title, MOVIE2K_URL, query):

	oc = ObjectContainer(title2=title)
	try:
		checkURL = query.split('/')[2]
		if checkURL != 'www.movie4k.to' and checkURL != '91.202.63.145' and checkURL != 'www.movie.to' and checkURL != 'movie4k.co.in' and checkURL != 'movie4k.to.come.in' and checkURL != 'www.movie4kunblocked.co' and checkURL != 'www.movie2kproxy.org' and checkURL != 'www.movie2kproxy.com' and checkURL != 'www.movie2k.tv' and checkURL != '91.202.62.123' and checkURL != 'www.movie2k.sx' and checkURL != 'www.movie2k.tl':
			return ObjectContainer(header="Not a Movie4k URL", message="The entered URL is not a valid Movie4k video URL. Example of a valid Movie4k video URL: http://www.movie4k.to/Oblivion-watch-movie-3777965.html  Please try again and click Ok to exit this screen.")
	except:
		return ObjectContainer(header="Not a Movie4k URL", message="The entered URL is not a valid Movie4k video URL. Example of a valid Movie4k video URL: http://www.movie4k.to/Oblivion-watch-movie-3777965.html  Please try again and click Ok to exit this screen.")

	session_cookies = Dict['_movie2k_uid']
	session_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	values = dict(session_token = Dict['_movie2k_uid'])
	
	req = requests.get(query, headers=session_headers, cookies=session_cookies)
	MOVIE_PAGE_HTML = HTML.ElementFromString(req.content)
	MOVIE_INFO = MOVIE_PAGE_HTML.xpath('//div[@id="details"]')[0].text_content()

	try:
		date = re.sub('[^0-9]', '', MOVIE_INFO.split('Year:')[1].split(':')[0])
		if date == "":
			date =  "0001"
	except:
		date = re.sub('[^0-9]', '', MOVIE_INFO.split('Land/Jahr:')[1].split(':')[0])
		if date == "":
			date =  "0001"
	try:
		MOVIE_INFO = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')
		lang = MOVIE_INFO[1].xpath("./span/img")[0].get('src').split('.')
		if len(lang) > 2:
			lang = lang[-2].split('/')[-1]
		else:
			lang = lang[0]
		MOVIES_LANG = GetLang(lang=lang)
	except:
		MOVIES_LANG = "N/A"

	try:
		MOVIES_TITLE = MOVIE_INFO[1].xpath("./span/h1/a")[0].text.strip()
	except:
		MOVIES_TITLE = MOVIE_INFO[1].xpath("./h1/span/a")[0].text.strip()
	try:
		MOVIES_QUALITY = MOVIE_INFO[1].xpath("./span/span/img")[0].get('title').split(' ')[2]
	except:
		MOVIES_QUALITY = "DVDRip/BDRip"

	if MOVIE2K_URL == "www.movie2k.sx":
		SiteURL = "http://www.movie2k.sx"
	else:
		SiteURL = ""
	MOVIES_THUMB = SiteURL + MOVIE_INFO[0].xpath("./a/img")[0].get('src')

	MOVIES_SUMMARY = "Year: "+date+" | Lang: "+MOVIES_LANG+" | Quality: "+MOVIES_QUALITY

	hosts = LoadData(fp=FAVORITES_DATA, GetJson=2)
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

	hosts = LoadData(fp=FAVORITES_DATA, GetJson=2)
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
		oc = ObjectContainer(header="We Apologize", message="This section does not contain any My Favorite videos to delete.")

	return oc


####################################################################################################
@route(PREFIX + '/DeleteURL')
def DeleteURL(title, page):

	oc = ObjectContainer(title2=title)

	hosts = LoadData(fp=FAVORITES_DATA, GetJson=2)
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
	return ObjectContainer(header="Deleted Movie2k URL", message="The Movie2k URL has been removed from My Favorites.  Please click Ok to exit this screen.")


####################################################################################################
@route(PREFIX + '/PlaybackDownloads')
def PlaybackDownloads(title):

	oc = ObjectContainer(title2=L(title), no_cache = True)

	hosts = LoadData(fp=WATCHIT_DATA, GetJson=3)
	i = 1
	for gethost in hosts:
		type = String.Unquote(gethost[i]['Type'], usePlus=True)
		dateadded = String.Unquote(gethost[i]['DateAdded'], usePlus=True)
		quality = gethost[i]['Quality']
		path = gethost[i]['Path']
		host = gethost[i]['Host']
		title = gethost[i]['Title']
		summary = String.Unquote(gethost[i]['Summary'], usePlus=True)
		genres = StripArray(String.Unquote(gethost[i]['Genres'], usePlus=True).split(','))
		directors = StripArray(String.Unquote(gethost[i]['Directors'], usePlus=True).split(','))
		guest_stars = StripArray(String.Unquote(gethost[i]['GuestStars'], usePlus=True).split(','))
		duration = gethost[i]['Duration']
		rating = float(gethost[i]['Rating'])
		index = int(gethost[i]['Index'])
		season = int(gethost[i]['Season'])
		content_rating = gethost[i]['ContentRating']
		source_title = gethost[i]['SourceTitle']
		originally_available_at = Datetime.ParseDate(String.Unquote(gethost[i]['Date'], usePlus=True), "%Y")
		thumb = String.Unquote(gethost[i]['ThumbURL'], usePlus=True)
		videotype = gethost[i]['VideoType']
		videostreamlink = gethost[i]['VideoStreamLink']
		HostPage = gethost[i]['HostPage']
		url = gethost[i]['URL']
		LinkType = gethost[i]['LinkType']
		contentlength = gethost[i]['ContentLength']
		FileCheckSize = gethost[i]['FileCheckSize']
		resumepath = gethost[i]['ResumePath']
		resumecontentlength = gethost[i]['ResumeContentLength']
		show = "ADDED: "+ dateadded + " | HOST: " + host + " | QUALITY: " + quality

		if duration != "None" and duration != "":
			duration = int(duration)
		else:
			duration = None

		if path != "":
			try:
				if resumepath == "":
					part = os.stat(path).st_size
					percent = 100 * float(part)/float(contentlength)

					LastTimeFileWrite = os.path.getmtime(path)
					LocalTime = time.time()
					ElapseTime = LocalTime - LastTimeFileWrite
				else:
					part = os.stat(path).st_size + os.stat(resumepath).st_size
					percent = 100 * float(part)/float(contentlength)

					if percent == 100.0:
						combine_files(parts=[path, resumepath], path=path.replace('Part1.', ''))
						gethost[i]['Path'] = path.replace('Part1.', '')
						gethost[i]['ResumePath'] = ""

					LastTimeFileWrite = os.path.getmtime(resumepath)
					LocalTime = time.time()
					ElapseTime = LocalTime - LastTimeFileWrite
			except:
				Log("Error: %s file not found to play back." % path)
				part = 0
				FileCheckSize = 0
				percent = 0.0
				ElapseTime = 120.0

			if percent == 100.0:
				path = os.path.abspath(path)
				if type == "TV Shows":
					oc.add(EpisodeObject(
							rating_key = path,
							key = Callback(PlaybackDownloadDetails, type=type, path=path, videotype=videotype, title=title, summary=summary, genres=genres, directors=directors, guest_stars=guest_stars, duration=duration, rating=rating, index=index, season=season, content_rating=content_rating, source_title=source_title, originally_available_at=originally_available_at, show=show, thumb=thumb),
							title = title,
							summary = summary,
							directors = directors,
							guest_stars = guest_stars,
							duration = duration,
							rating = rating,
							show = show,
							index = index,
							season = season,
							content_rating = content_rating,
							source_title = source_title,
							originally_available_at = originally_available_at,
							thumb = Callback(GetThumb, url=thumb),
							items = MediaObjectsForURL(path, videotype)))
				else:
					oc.add(MovieObject(
							rating_key = path,
							key = Callback(PlaybackDownloadDetails, type=type, path=path, videotype=videotype, title=title, summary=summary, genres=genres, directors=directors, guest_stars=guest_stars, duration=duration, rating=rating, index=index, season=season, content_rating=content_rating, source_title=source_title, originally_available_at=originally_available_at, show=show, thumb=thumb),
							title = title,
							summary = summary,
							directors = directors,
							genres = genres,
							duration = duration,
							rating = rating,
							content_rating = content_rating,
							source_title = show,
							originally_available_at = originally_available_at,
							thumb = Callback(GetThumb, url=thumb),
							items = MediaObjectsForURL(path, videotype)))
			elif ElapseTime >= 120.0 and int(FileCheckSize) == part:

				if HostVideoDownload.stop == None:
					HostVideoDownload.stop = CheckForDownload()
				jj = 0
				while jj < 4:
					(HostVideoDownload.MyDownloadPath, HostVideoDownload.MyDownloadRequest, ResumeContentLength, GoodLink, VideoStreamLink) = ResumeMyDownload(Host=host, HostPage=HostPage, url=url, LinkType=LinkType, path=path, ContentLength=contentlength)
					if GoodLink != True:
						time.sleep(1)
						jj += 1
					else:
						jj = 4

				if int(ResumeContentLength) != int(contentlength) and GoodLink == True:
					if not "Part1." in path:
						os.renames(path, path.replace(DownloadPath, DownloadPath+'Part1.'))
						gethost[i]['Path'] = path.replace(DownloadPath, DownloadPath+'Part1.')
					gethost[i]['ResumePath'] = HostVideoDownload.MyDownloadPath
					gethost[i]['ResumeContentLength'] = ResumeContentLength

				if GoodLink == True:
					gethost[i]['FileCheckSize'] = "0"
					JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)
					oc.add(DirectoryObject(key=Callback(WatchitDownloadInfo, title=title), title=title, summary=show, thumb=Callback(GetThumb, url=thumb)))
				else:
					oc.add(DirectoryObject(key=Callback(WatchitDownloadInfo, title=title, GoodLink=GoodLink), title=title, summary=show, thumb=Callback(GetThumb, url=thumb)))
			else:
				gethost[i]['FileCheckSize'] = str(part)
				JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)
				oc.add(DirectoryObject(key=Callback(WatchitDownloadInfo, title=title, percent=percent), title=title, summary=show, thumb=Callback(GetThumb, url=thumb)))

		i += 1

	if len(oc) < 1:
		oc = ObjectContainer(header="We Apologize", message="This section does not contain any Watchit Later videos.  Please add a video to view.")

	return oc


####################################################################################################
@route(PREFIX + '/PlaybackDownloadDetails')
def PlaybackDownloadDetails(type, path, videotype, title, summary, genres, directors, guest_stars, duration, rating, index, season, content_rating, source_title, originally_available_at, show, thumb, maxVideoBitrate=None, videoQuality=None, directPlay=None, audioBoost=None, partIndex=None, waitForSegments=None, session=None, offset=None, videoResolution=None, subtitleSize=None, directStream=None):
	title = unicode(title, errors='replace')
	summary = unicode(summary, errors='replace')
	oc = ObjectContainer(title2=title)

	originally_available_at = Datetime.ParseDate(originally_available_at, "%Y")
	directors = [directors]
	guest_stars = [guest_stars]
	genres = [genres]
	duration = int(duration)
	rating = float(rating)
	season = int(season)
	index = int(index)

	if type == "TV Shows":
		oc.add(EpisodeObject(
				rating_key = path,
				key = Callback(PlaybackDownloadDetails, type=type, path=path, videotype=videotype, title=title, summary=summary, genres=genres, directors=directors, guest_stars=guest_stars, duration=duration, rating=rating, index=index, season=season, content_rating=content_rating, source_title=source_title, originally_available_at=originally_available_at, show=show, thumb=thumb),
				title = title,
				summary = summary,
				directors = directors,
				guest_stars = guest_stars,
				duration = duration,
				rating = rating,
				show = show,
				index = index,
				season = season,
				content_rating = content_rating,
				source_title = source_title,
				originally_available_at = originally_available_at,
				thumb = Callback(GetThumb, url=thumb),
				items = MediaObjectsForURL(path, videotype)))
	else:
		oc.add(MovieObject(
				rating_key = path,
				key = Callback(PlaybackDownloadDetails, type=type, path=path, videotype=videotype, title=title, summary=summary, genres=genres, directors=directors, guest_stars=guest_stars, duration=duration, rating=rating, index=index, season=season, content_rating=content_rating, source_title=source_title, originally_available_at=originally_available_at, show=show, thumb=thumb),
				title = title,
				summary = summary,
				directors = directors,
				genres = genres,
				duration = duration,
				rating = rating,
				content_rating = content_rating,
				source_title = show,
				originally_available_at = originally_available_at,
				thumb = Callback(GetThumb, url=thumb),
				items = MediaObjectsForURL(path, videotype)))

	return oc



####################################################################################################
@route(PREFIX + '/MediaObjectsForURL')
def MediaObjectsForURL(path, videotype):

	if videotype == 'mp4':
		video_frame_rate = "30"
		video_resolution = Prefs['video_resolution']
		container = Container.MP4
		video_codec = VideoCodec.H264
		audio_codec = AudioCodec.AAC
		audio_channels = 2
		bitrate = None
		optimized_for_streaming = True
	elif videotype == 'flv':
		video_frame_rate = "30"
		video_resolution = Prefs['video_resolution']
		container = Container.FLV
		video_codec = VideoCodec.VP6
		audio_codec = AudioCodec.MP3
		bitrate = None
		audio_channels = 2
		optimized_for_streaming = True
	else:
		video_frame_rate = "30"
		video_resolution = Prefs['video_resolution']
		container = None
		video_codec = None
		audio_codec = None
		bitrate = None
		audio_channels = 2
		optimized_for_streaming = True

	obj = [MediaObject(
			video_frame_rate = video_frame_rate,
			video_resolution = video_resolution,
			container = container,
			video_codec = video_codec,
			audio_codec = video_codec,
			bitrate = bitrate,
			audio_channels = audio_channels,
			optimized_for_streaming = optimized_for_streaming,
			parts = [PartObject(key=Callback(PlayVideo, path=path))]
		)]

	return obj


###################################################################################################
@indirect
def PlayVideo(path):

	oc = ObjectContainer()

	oc.add(VideoClipObject(
		items = [
				MediaObject(
					parts = [PartObject(key=Callback(CreateLocalURL, path=path))]
				)
        		]
	))

	return oc


###################################################################################################
@route(PREFIX + '/CreateLocalURL')
def CreateLocalURL(path, *argparams, **kwparams):
	return Redirect(Stream.LocalFile(path))


####################################################################################################
@route(PREFIX + '/WatchitDownloadInfo')
def WatchitDownloadInfo(title, percent=None, GoodLink=True):
	if percent != None:
		oc = ObjectContainer(header=title+" Still Downloading", message="Your video download is still in progress.  Please check back later.  DOWNLOAD PERCENTAGE: "+str(percent)+"%")
	elif GoodLink != True:
		oc = ObjectContainer(header="We Apologize", message="There was a problem with the Host video resuming download.  Host video errored do to "+GoodLink+".  Please try again later to resume download.")
	else:
		oc = ObjectContainer(header=title+" Resuming Download", message="Your video stopped downloading and now resuming your video download.  Please check back later.")

	return oc


####################################################################################################
@route(PREFIX + '/DeleteWatchitLaterVideo')
def DeleteWatchitLaterVideo(title):

	oc = ObjectContainer(title2=title)

	hosts = LoadData(fp=WATCHIT_DATA, GetJson=3)
	i = 1
	for gethost in hosts:
		dateadded = String.Unquote(gethost[i]['DateAdded'], usePlus=True)
		quality = gethost[i]['Quality']
		path = gethost[i]['Path']
		host = gethost[i]['Host']
		title = gethost[i]['Title']
		thumb = String.Unquote(gethost[i]['ThumbURL'], usePlus=True)
		summary = "ADDED: "+ dateadded + " | HOST: " + host + " | QUALITY: " + quality
		i += 1

		if path != "":
			oc.add(DirectoryObject(key=Callback(DeleteVideo, title=title, path=path), title=title, summary=summary, thumb=Callback(GetThumb, url=thumb)))

	if len(oc) < 1:
		oc = ObjectContainer(header="We Apologize", message="This section does not contain any My Watchit Later videos to delete.")

	return oc


####################################################################################################
@route(PREFIX + '/DeleteVideo')
def DeleteVideo(title, path):

	title = unicode(title, errors='replace')
	oc = ObjectContainer(title2=title)

	hosts = LoadData(fp=WATCHIT_DATA, GetJson=3)
	i = 1
	for gethost in hosts:
		if gethost[i]['Path'] == path:
			gethost[i]['Type'] = ""
			gethost[i]['DateAdded'] = ""
			gethost[i]['Quality'] = ""
			gethost[i]['Path'] = ""
			gethost[i]['Host'] = ""
			gethost[i]['Title'] = ""
			gethost[i]['Summary'] = ""
			gethost[i]['Genres'] = ""
			gethost[i]['Directors'] = ""
			gethost[i]['GuestStars'] = ""
			gethost[i]['Duration'] = ""
			gethost[i]['Rating'] = "0.0"
			gethost[i]['Index'] = "0"
			gethost[i]['Season'] = "0"
			gethost[i]['ContentRating'] = ""
			gethost[i]['SourceTitle'] = ""
			gethost[i]['Date'] = ""
			gethost[i]['ThumbURL'] = ""
			gethost[i]['VideoType'] = ""
			gethost[i]['VideoStreamLink'] = ""
			gethost[i]['HostPage'] = ""
			gethost[i]['URL'] = ""
			gethost[i]['LinkType'] = ""
			gethost[i]['ContentLength'] = ""
			gethost[i]['FileCheckSize'] = "0"
			gethost[i]['ResumePath'] = ""
			gethost[i]['ResumeContentLength'] = ""
			KillMyDownloadThread(MyThread=gethost[i]['Thread'])
			gethost[i]['Thread'] = ""
			break
		else:
			i += 1

	if os.path.isfile(path):
		try:
			os.remove(path)
		except OSError:
			gethost[i]['FailedFileDeletion'] = path
            		Log("Unable to remove file: %s" % path)
	else:
		Log("Error: %s file not found to remove." % path)

	JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)
	return ObjectContainer(header="Deleted Movie2k Host Video", message="The Movie2k, " + title + " Video has been removed from My Watchit Later.  Please click Ok to exit this screen.")


####################################################################################################
def CheckFailedFileDeletions():

	hosts = LoadData(fp=WATCHIT_DATA, GetJson=3)
	i = 1
	for gethost in hosts:
		try:
			path = gethost[i]['FailedFileDeletion']
		except:
			gethost[i].update({'FailedFileDeletion': ''})
			path = ""

		if path != "":
			if os.path.isfile(path):
				try:
					os.remove(path)
					gethost[i]['FailedFileDeletion'] = ""
				except OSError:
            				Log("Unable to remove file: %s" % path)
			else:
				Log("Error: %s file not found to remove." % path)

		#Fix any patch issues between plugin updates if dictionary has changed.
		try:
			gethost[i]['Type']
		except:
			gethost[i].update({'Type': ''})
		try:
			gethost[i]['DateAdded']
		except:
			gethost[i].update({'DateAdded': ''})
		try:
			gethost[i]['Quality']
		except:
			gethost[i].update({'Quality': ''})
		try:
			gethost[i]['Path']
		except:
			gethost[i].update({'Path': ''})
		try:
			gethost[i]['Host']
		except:
			gethost[i].update({'Host': ''})
		try:
			gethost[i]['Title']
		except:
			gethost[i].update({'Title': ''})
		try:
			gethost[i]['Summary']
		except:
			gethost[i].update({'Summary': ''})
		try:
			gethost[i]['Genres']
		except:
			gethost[i].update({'Genres': ''})
		try:
			gethost[i]['Directors'] = ""
		except:
			gethost[i].update({'Directors': ''})
		try:
			gethost[i]['GuestStars']
		except:
			gethost[i].update({'GuestStars': ''})
		try:
			gethost[i]['Duration']
		except:
			gethost[i].update({'Duration': ''})
		try:
			gethost[i]['Rating']
		except:
			gethost[i].update({'Rating': '0.0'})
		try:
			gethost[i]['Index']
		except:
			gethost[i].update({'Index': '0'})
		try:
			gethost[i]['Season']
		except:
			gethost[i].update({'Season': '0'})
		try:
			gethost[i]['ContentRating']
		except:
			gethost[i].update({'ContentRating': ''})
		try:
			gethost[i]['SourceTitle']
		except:
			gethost[i].update({'SourceTitle': ''})
		try:
			gethost[i]['Date']
		except:
			gethost[i].update({'Date': ''})
		try:
			gethost[i]['ThumbURL']
		except:
			gethost[i].update({'ThumbURL': ''})
		try:
			gethost[i]['VideoType']
		except:
			gethost[i].update({'VideoType': ''})
		try:
			gethost[i]['VideoStreamLink']
		except:
			gethost[i].update({'VideoStreamLink': ''})
		try:
			gethost[i]['HostPage']
		except:
			gethost[i].update({'HostPage': ''})
		try:
			gethost[i]['URL']
		except:
			gethost[i].update({'URL': ''})
		try:
			gethost[i]['LinkType']
		except:
			gethost[i].update({'LinkType': ''})
		try:
			gethost[i]['ContentLength']
		except:
			gethost[i].update({'ContentLength': ''})
		try:
			gethost[i]['FileCheckSize']
		except:
			gethost[i].update({'FileCheckSize': '0'})
		try:
			gethost[i]['ResumePath']
		except:
			gethost[i].update({'ResumePath': ''})
		try:
			gethost[i]['ResumeContentLength']
		except:
			gethost[i].update({'ResumeContentLength': ''})
		try:
			gethost[i]['Thread']
		except:
			gethost[i].update({'Thread': ''})

		i += 1

	JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)


####################################################################################################
@route(PREFIX + '/Queue')
def Queue(title, loginResult, MOVIE2K_URL):

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
def Messages(title, loginResult, MOVIE2K_URL):

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

				oc.add(DirectoryObject(key = Callback(ShowMessage, title=title, url=url, summary=summary2, MOVIE2K_URL=MOVIE2K_URL), title = title, summary=summary, thumb=MYMESSAGES_THUMB))
				i += 1
		except:
			oc = ObjectContainer(header="User Login Error", message="Your user login and password are correct but there has been an error connecting to the website user account.  Please click ok to exit this screen and the back button to refresh login data. (MAY TAKE SEVERAL TRIES)")
	else:
		oc = ObjectContainer(header="User Login Required", message="Please enter your Movie4k login username and password in Preferences.  If you do not have an account please go to www.movie4k.to and click the Register link at the very top of the page to create you a new account.")

	return oc


####################################################################################################
def ShowMessage(title, url, summary, MOVIE2K_URL):

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
def TVShows(title, type, MOVIE2K_URL):
	
	oc = ObjectContainer(title2=title)

	#Add Featured TV Show
	ICON_FEATURED = "icon-latest-featured.png"
	TVSHOW_TITLE = "Featured TV Shows"
	TVSHOW_SUMMARY = "Your Featured TV Shows in the Movie2k database!"
	TVSHOW_THUMB = R(ICON_FEATURED)
	if MOVIE2K_URL == "www.movie2k.sx":
		TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/series"
	else:
		TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/tvshows_featured.php"
	oc.add(DirectoryObject(key=Callback(FeaturedTVShowsPageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))

	#Add Latest Updates TV Show
	Genre_Type = "Latest Updates"
	ICON_UPDATES = "icon-latest-updates.png"
	TVSHOW_TITLE = "Newly Added TV Shows"
	TVSHOW_SUMMARY = "Your Latest Updates to the TV Shows database!"
	TVSHOW_THUMB = R(ICON_UPDATES)
	TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/tvshows-updates.html"
	if MOVIE2K_URL == "www.movie2k.sx":
		oc.add(DirectoryObject(key=Callback(DisabledScreen, title=TVSHOW_TITLE, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))
	else:
		oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))

	#Add Alphabitical listing to TV Show
	Genre_Type = "Alphabitical Listing"
	ICON_ALPHA = "icon-alphabetical.png"
	TVSHOW_TITLE = "Alphabitical listing of the TV Shows"
	TVSHOW_SUMMARY = "Listings sorted by Alphabitical order of the TV Shows database!"
	TVSHOW_THUMB = R(ICON_ALPHA)
	TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/tvshows-all.html"
	if MOVIE2K_URL == "www.movie2k.tl":
		oc.add(DirectoryObject(key=Callback(TVShowsList, title=TVSHOW_TITLE, page=TVSHOW_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))
	elif MOVIE2K_URL == "www.movie2k.sx":
		oc.add(DirectoryObject(key=Callback(AlphabiticalPageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))	
	else:
		oc.add(DirectoryObject(key=Callback(AlphabiticalTVShowsPageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))

	#Add Genre Pages to TV Page
	ICON_GENRE = "icon-genre.png"
	TVSHOW_TITLE = "Genre listing of TV Shows"
	TVSHOW_SUMMARY = "Listings sorted by Genre of the TV Shows database!"
	TVSHOW_THUMB = R(ICON_GENRE)
	TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/genres-tvshows.html"
	oc.add(DirectoryObject(key=Callback(GenreTVShowsPageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))

	if MOVIE2K_URL == "www.movie2k.tl" or Prefs['toppages'] == "Enabled":
		#Add Top TV Shows
		Genre_Type = "Top TV Shows"
		ICON_UPDATES = "icon-top.png"
		TVSHOW_TITLE = "Top TV Shows"
		TVSHOW_SUMMARY = "Your Top TV Shows in the Movie2k database!"
		TVSHOW_THUMB = R(ICON_UPDATES)
		TVSHOW_PAGE = "http://" + MOVIE2K_URL + "/tvshows-top.html"
		if MOVIE2K_URL == "www.movie2k.sx":
			oc.add(DirectoryObject(key=Callback(DisabledScreen, title=TVSHOW_TITLE, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))
		else:
			oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=TVSHOW_TITLE, page=TVSHOW_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=TVSHOW_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/AlphabiticalTVShowsPageAdd')
def AlphabiticalTVShowsPageAdd(title, page, type, MOVIE2K_URL):

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

	oc.add(DirectoryObject(key=Callback(TVShowsList, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Alpha_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	for AlphNumeric in HTML.ElementFromString(req.content).xpath('//div[@id="content"]/div[@id="boxgrey"]'):
		Alpha_Type = AlphNumeric.xpath('./a')[0].text
		ICON_MOVIES = "icon-"+Alpha_Type.lower()+".png"
		MOVIES_TITLE = Alpha_Type+" "+type
		MOVIES_SUMMARY = "Your "+Alpha_Type+" list of the "+type+" database!"
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE = AlphNumeric.xpath('./a')[0].get('href')

		oc.add(DirectoryObject(key=Callback(TVShowsList, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Alpha_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/GenreTVShowsPageAdd')
def GenreTVShowsPageAdd(title, page, type, MOVIE2K_URL):

	oc = ObjectContainer(title2=title)

	if MOVIE2K_URL == "www.movie2k.tl":
		return ObjectContainer(header="We Apologize", message="This section does not contain any Genre TVShows listings do to problem no content generation from www.movie2k.tl genre page.")
	elif MOVIE2K_URL == "www.movie2k.sx":
		elm = 'div[@id="maincontent4"]/table[@id="tablemoviesindex"]'
	else:
		elm = 'div[@id="content"]/table[@id="tablemovies"]'

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)

	NotSkip = True

	for Genre in HTML.ElementFromString(req.content).xpath('//' + elm + '/tr'):
		Genre_Type = Genre.xpath('./td[@id="tdmovies"]/a')[0].text
		ICON_MOVIES = "icon-"+Genre_Type.lower()+".png"
		MOVIES_TITLE = Genre_Type+" "+type
		MOVIES_SUMMARY = "Your "+Genre_Type+" TV Shows database!"
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/"+Genre.xpath('./td[@id="tdmovies"]/a')[0].get('href')

		if DisableAdult() != True and Genre_Type.lower() == 'adult':
			NotSkip = False

		if NotSkip:
			if MOVIE2K_URL == "www.movie2k.sx":
				oc.add(DirectoryObject(key=Callback(MovieGenres, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, thumb=MOVIES_THUMB, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
			else:
				oc.add(DirectoryObject(key=Callback(TVShowsList, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
		else:
			NotSkip = True

	return oc


####################################################################################################
@route(PREFIX + '/TVShowsList')
def TVShowsList(title, page, genre, type, MOVIE2K_URL):
	
	oc = ObjectContainer(title2=title)

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)

	if MOVIE2K_URL == "www.movie2k.tl":
		elm = '/tbody'
	else:
		elm = ''

	for List in HTML.ElementFromString(req.content).xpath('//div[@id="maincontent4"]/table[@id="tablemoviesindex"]'+elm+'/tr'):
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
		MOVIES_TITLE = MOVIES_TD[0].xpath('./a')[0].text.strip()
		MOVIES_SUMMARY = "Lang: "+MOVIES_LANG+" | Part of the "+genre+" TV Show line up on Movie2k."
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/"+MOVIES_TD[0].xpath('./a')[0].get('href')

		if MOVIES_LANG == GetLanguage() or MOVIES_LANG == 'N/A' or GetLanguage() == 'All':
			oc.add(DirectoryObject(key=Callback(TVShowSeasons, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=genre, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/FeaturedTVShowsPage')
def FeaturedTVShowsPageAdd(title, page, type, MOVIE2K_URL):
	
	oc = ObjectContainer(title2=title)
	
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)

	FEATURED_TVSHOW_PAGE = HTML.ElementFromString(req.content)
	dateadd = 'N/A'
	TVSHOWS_DIV = FEATURED_TVSHOW_PAGE.xpath('//div[@id="maincontenttvshow"]/div')
	TVShowsLength = len(TVSHOWS_DIV)
	if MOVIE2K_URL == "www.movie2k.sx":
		SiteURL = "http://www.movie2k.sx"
	else:
		SiteURL = ""

	i = 0
	while i < TVShowsLength:
		TVSHOW_THUMB = SiteURL + TVSHOWS_DIV[i].xpath("./a/img")[0].get('src')
		TVSHOW_TITLE = TVSHOWS_DIV[i].xpath("./a/img")[0].get('title')
		i += 1
		TVSHOW_TITLE = TVSHOW_TITLE
		if MOVIE2K_URL == "www.movie2k.sx":
			TVSHOW_PAGE = SiteURL + TVSHOWS_DIV[i-1].xpath("./a")[0].get('href')
		else:
			TVSHOW_PAGE = TVSHOWS_DIV[i].xpath('./div[@class="beschreibung"]/table[@id="tablemoviesindex"]//a')[0].get('href')
		TVSHOW_YEAR_SUB = TVSHOWS_DIV[i].xpath('./div[@class="beschreibung"]/span')[0]
		TVSHOW_YEAR = re.sub('[^0-9]', '', TVSHOW_YEAR_SUB.text_content().split('Year:')[1])
		LANGUAGE_URL = TVSHOWS_DIV[i].xpath("./h2//img")[0].get('src')
		try:
			try:
				TVSHOW_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
			except:
				TVSHOW_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
		except:
			TVSHOW_LANG = GetLang(lang=LANGUAGE_URL.split('/')[1].split('.')[0])
		TVSHOW_SUMMARY = "Year: "+TVSHOW_YEAR+" | Lang: "+TVSHOW_LANG+" | Part of the Featured TV Show line up on Movie2k."
		i += 2

		oc.add(DirectoryObject(key=Callback(TVShowSeasons, title=TVSHOW_TITLE, page=TVSHOW_PAGE, genre="N/A", type=type, MOVIE2K_URL=MOVIE2K_URL, thumb=TVSHOW_THUMB, MOVIES_LANG=TVSHOW_LANG), title=TVSHOW_TITLE, summary=TVSHOW_SUMMARY, thumb=Callback(GetThumb, url=TVSHOW_THUMB)))

	return oc


####################################################################################################
@route(PREFIX + '/TVShowSeasons')
def TVShowSeasons(title, page, genre, type, MOVIE2K_URL, thumb=None, MOVIES_LANG=None):
	
	oc = ObjectContainer(title2=title)

	if page.split('/')[0] != "http:":
		page = "http://"+MOVIE2K_URL+"/"+page

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)
	MOVIE_PAGE = HTML.ElementFromString(req.content)

	if MOVIE2K_URL == "www.movie2k.sx":
		SEASON = '//select[@id="season"]/option'
	else:
		if MOVIE2K_URL == "www.movie2k.tl":
			elm = '/tbody'
		else:
			elm = ''
		if thumb == None:
			SEASON = '//div[@id="maincontent4"]/table[@id="tablemoviesindex"]'+elm+'/tr'
		else:
			if thumb == "N/A":
				thumb = None
			SEASON = '//select[@name="season"]/option'


	for Seasons in MOVIE_PAGE.xpath(SEASON):
		if MOVIES_LANG == None:
			MOVIES_TD = Seasons.xpath('./td[@id="tdmovies"]')
			try:
				LANGUAGE_URL = MOVIES_TD[1].xpath("./img")[0].get('src')
				try:
					MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[5].split('.')[0])
				except:
					MOVIES_LANG = GetLang(lang=LANGUAGE_URL.split('/')[4].split('.')[0])
			except:
				MOVIES_LANG = "N/A"
			MOVIES_TITLE = re.sub('\t', '', MOVIES_TD[0].xpath('./a')[0].text).replace('  ', '').replace(',', ', ').replace(':', ': ')
			MOVIES_PAGE = "http://" + MOVIE2K_URL + "/"+MOVIES_TD[0].xpath('./a')[0].get('href')
			CSRF_TOKEN = None
			MOVIES_LANG_B = None
			HasSeason = True
		else:
			try:
				try:
					MOVIES_TITLE = title + ", " + Seasons.text.replace(' ', ': ')
					MOVIES_PAGE = "http://www.movie2k.sx/seasons/" + Seasons.get('value') + "/get_episodes"
					CSRF_TOKEN = MOVIE_PAGE.xpath('//meta[@name="csrf-token"]')[0].get('content')
					MOVIES_LANG_B = MOVIES_LANG
					HasSeason = True
				except:
					MOVIES_TITLE = title + ", " + Seasons.text.replace(' ', ': ')
					MOVIES_PAGE = page
					CSRF_TOKEN = None
					MOVIES_LANG_B = MOVIES_LANG
					HasSeason = True
			except:
				HasSeason = False

		if thumb == None:
			ICON_MOVIES = "icon-"+genre.lower()+".png"
			MOVIES_THUMB = R(ICON_MOVIES)
		else:
			MOVIES_THUMB = Callback(GetThumb, url=thumb)
		
		if HasSeason == True:
			MOVIES_SUMMARY = "Lang: "+MOVIES_LANG+" | Part of the "+genre+" TV Shows season line up on Movie2k."
			oc.add(DirectoryObject(key=Callback(TVShowEpisodes, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=genre, type=type, MOVIE2K_URL=MOVIE2K_URL, thumb=thumb, MOVIES_LANG_B=MOVIES_LANG_B, CSRF_TOKEN=CSRF_TOKEN), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	if len(oc) < 1:
		oc = ObjectContainer(header="We Apologize", message=title + " does not have any Host sites listed for video playback.  Try again later to see if Movie2k site adds any Hosts.")

	return oc


####################################################################################################
@route(PREFIX + '/TVShowEpisodes')
def TVShowEpisodes(title, page, genre, type, MOVIE2K_URL, thumb=None, MOVIES_LANG_B=None, CSRF_TOKEN=None):
	
	oc = ObjectContainer(title2=title)

	cookies = Dict['_movie2k_uid']
	if CSRF_TOKEN == None:
		headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}

		if MOVIE2K_URL == "www.movie2k.tl":
			elm = '/tbody'
		else:
			elm = ''
		if MOVIES_LANG_B == None:
			EPISODE = '//div[@id="maincontent4"]/table[@id="tablemoviesindex"]'+elm+'/tr'
			THUMB = 0
		else:
			whichSeason = title.split('Season:')[1].strip()
			EPISODE = '//form[@name="episodeform'+whichSeason+'"]/select/option'
			THUMB = 1
	else:
		headers = {"Accept": "text/javascript, application/javascript", "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum], "X-CSRF-Token": CSRF_TOKEN, "X-Requested-With": "XMLHttpReques"}
		EPISODE = '//select[@id="episode"]/option'
		THUMB = 1

	req = requests.get(page, headers=headers, cookies=cookies)

	if CSRF_TOKEN != None:
		headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
		page = "http://www.movie2k.sx" + req.content.split("'")[1]
		req = requests.get(page, headers=headers, cookies=cookies)

	MOVIE_PAGE = HTML.ElementFromString(req.content)
	MOVIES_THUMB = thumb

	for Episodes in MOVIE_PAGE.xpath(EPISODE):
		if MOVIES_LANG_B == None:
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
			MOVIES_TITLE = re.sub('\t', '', MOVIES_TD[0].xpath('./a')[0].text).replace('  ', '').replace(',', ', ').replace(':', ': ')
			MOVIES_PAGE = MOVIES_TD[0].xpath('./a')[0].get('href')
			HasEpisode = True
		else:
			try:
				try:
					DATE_ADDED = 'N/A'
					MOVIES_LANG = MOVIES_LANG_B
					MOVIES_TITLE = title + ",  " + Episodes.text.replace(' ', ': ')
					MOVIES_PAGE = "http://www.movie2k.sx/episodes/" + Episodes.get('value') + "/get_links"
					CSRF_TOKEN = MOVIE_PAGE.xpath('//meta[@name="csrf-token"]')[0].get('content')
					HasEpisode = True
				except:
					DATE_ADDED = 'N/A'
					MOVIES_LANG = MOVIES_LANG_B
					MOVIES_TITLE = title + ",  " + Episodes.text.replace(' ', ': ')
					MOVIES_PAGE = Episodes.get('value')
					HasEpisode = True
			except:
				HasEpisode = False

		if THUMB == 0:
			page = "http://"+MOVIE2K_URL+"/"+MOVIES_PAGE
			req = requests.get(page, headers=headers, cookies=cookies)
			GET_THUMB = HTML.ElementFromString(req.content).xpath('//div[@id="maincontent5"]/div/div')[0]
			MOVIES_THUMB = GET_THUMB.xpath('./a/img')[0].get('src')
			THUMB = 1

		if HasEpisode == True:
			MOVIES_SUMMARY = "Added: "+DATE_ADDED+" | Lang: "+MOVIES_LANG+" | Part of the "+genre+" TV Shows episode line up on Movie2k."
			oc.add(DirectoryObject(key=Callback(SubGroupMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=DATE_ADDED, dateadd=DATE_ADDED, thumbck=MOVIES_THUMB, type=type, summary=MOVIES_SUMMARY, MOVIE2K_URL=MOVIE2K_URL, CSRF_TOKEN=CSRF_TOKEN), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))

	return oc


####################################################################################################
@route(PREFIX + '/Movie')
def Movies(title, type, MOVIE2K_URL):
	
	oc = ObjectContainer(title2=title)

	Genre_Type = "Latest Updates"
	ICON_UPDATES = "icon-latest-updates.png"

	if type == 'Movies':
		#Add Newly Added Cinema Movies Page
		ICON_CINEMA = "icon-cinema.png"
		MOVIES_TITLE = "Newly Added Cinema Movies"
		MOVIES_SUMMARY = "Your Latest Updates to the Cinema Movies database!"
		MOVIES_THUMB = R(ICON_CINEMA)
		if MOVIE2K_URL == "www.movie2k.tl":
			MOVIES_PAGE = "http://" + MOVIE2K_URL
		elif MOVIE2K_URL == "www.movie2k.sx":
			MOVIES_PAGE = "http://" + MOVIE2K_URL + "/movies"
		elif GetLanguage() == "German":
			MOVIES_PAGE = "http://" + MOVIE2K_URL + "/index.php?lang=de"
		else:
			MOVIES_PAGE = "http://" + MOVIE2K_URL + "/index.php?lang=us"
		oc.add(DirectoryObject(key=Callback(CinemaMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		#Add Latest Updates Movie Page
		MOVIES_TITLE = "Newly Added Movies"
		MOVIES_SUMMARY = "Your Latest Updates to the Movies database!"
		MOVIES_THUMB = R(ICON_UPDATES)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/movies-updates.html"
		if MOVIE2K_URL == "www.movie2k.tl":
			oc.add(DirectoryObject(key=Callback(MovieGenres, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, thumb=MOVIES_THUMB, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
		else:
			oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		#Add By Alphabitical listing Movie Page
		ICON_ALPHA = "icon-alphabetical.png"
		MOVIES_TITLE = "Alphabitical listing of Movies"
		MOVIES_SUMMARY = "Listings sorted by Alphabitical order of the Movies database!"
		MOVIES_THUMB = R(ICON_ALPHA)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/movies-all.html"
		oc.add(DirectoryObject(key=Callback(AlphabiticalPageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		#Add By Genre listing Movie Page
		ICON_GENRE = "icon-genre.png"
		MOVIES_TITLE = "Genre listing of Movies"
		MOVIES_SUMMARY = "Listings sorted by Genre of the Movies database!"
		MOVIES_THUMB = R(ICON_GENRE)
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/genres-movies.html"
		oc.add(DirectoryObject(key=Callback(GenrePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

		if MOVIE2K_URL == "www.movie2k.tl" or Prefs['toppages'] == "Enabled":
			#Add Top Movies
			Genre_Type = "Top Movies"
			ICON_TOP = "icon-top.png"
			MOVIES_TITLE = "Top Movies"
			MOVIES_SUMMARY = "Your Top Movies in the Movie2k database!"
			MOVIES_THUMB = R(ICON_TOP)
			MOVIES_PAGE = "http://" + MOVIE2K_URL + "/movies-top.html"
			if MOVIE2K_URL == "www.movie2k.sx":
				oc.add(DirectoryObject(key=Callback(DisabledScreen, title=MOVIES_TITLE, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
			else:
				oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	elif type == 'XXX Movies':
		if MOVIE2K_URL == "www.movie2k.tl" or MOVIE2K_URL == "www.movie2k.sx":
			return ObjectContainer(header="We Apologize", message="This section has been disabled do to "+ MOVIE2K_URL +" disabling it on their site.")

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
			oc.add(InputDirectoryObject(key=Callback(InputParentalPassword, title=title, type=type, MOVIE2K_URL=MOVIE2K_URL), title=title, summary=summary, thumb=PARENTAL_THUMB, prompt=prompt))
		else:

			#Add Featured XXX Movie Page
			ICON_FEATURED = "icon-latest-featured.png"
			PORN_TITLE = "Featured XXX Movies"
			PORN_SUMMARY = "Your Featured Movies in the XXX Movies database!"
			PORN_THUMB = R(ICON_FEATURED)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-updates.html"
			oc.add(DirectoryObject(key=Callback(FeaturedMoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add Latest Updates XXX Movie Page
			PORN_TITLE = "Newly Added XXX Movies"
			PORN_SUMMARY = "Your Latest Updates to the XXX Movies database!"
			PORN_THUMB = R(ICON_UPDATES)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-updates.html"
			oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add By Alphabitical listing XXX Movie Page
			ICON_ALPHA = "icon-alphabetical.png"
			PORN_TITLE = "Alphabitical listing of XXX Movies"
			PORN_SUMMARY = "Listings sorted by Alphabitical order of the XXX Movies database!"
			PORN_THUMB = R(ICON_ALPHA)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-all.html"
			oc.add(DirectoryObject(key=Callback(AlphabiticalPageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add By Genre listing XXX Movie Page
			ICON_GENRE = "icon-genre.png"
			PORN_TITLE = "Genre listing of XXX Movies"
			PORN_SUMMARY = "Listings sorted by Genre of the XXX Movies database!"
			PORN_THUMB = R(ICON_GENRE)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/genres-xxx.html"
			oc.add(DirectoryObject(key=Callback(GenrePageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			if Prefs['toppages'] == "Enabled":
				#Add Top XXX Movies
				Genre_Type = "Top XXX Movies"
				ICON_TOP = "icon-top.png"
				MOVIES_TITLE = "Top Movies"
				MOVIES_SUMMARY = "Your Top XXX Movies in the Movie2k database!"
				MOVIES_THUMB = R(ICON_TOP)
				MOVIES_PAGE = "http://" + MOVIE2K_URL + "/xxx-top.html"
				oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/InputParentalPassword')
def InputParentalPassword(title, type, MOVIE2K_URL, query):

	oc = ObjectContainer(title2=title)

	ParentalLock = Prefs["parentallock"]
	Password = LoadData(fp=CAPTCHA_DATA)
	ParentalPassword = Password[0][1]['ParentalPassword']
	PasswordCheck = ParentalPassword.decode('base64', 'strict')

	if ParentalLock == "Enabled" and ParentalPassword == "":
		Password[0][1]['ParentalPassword'] = query.encode('base64', 'strict').replace('\n', '')
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
			oc.add(DirectoryObject(key=Callback(FeaturedMoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add Latest Updates XXX Movie Page
			Genre_Type = "Latest Updates"
			ICON_UPDATES = "icon-latest-updates.png"
			PORN_TITLE = "Newly Added XXX Movies"
			PORN_SUMMARY = "Your Latest Updates to the XXX Movies database!"
			PORN_THUMB = R(ICON_UPDATES)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-updates.html"
			oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=PORN_TITLE, page=PORN_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add By Alphabitical listing XXX Movie Page
			ICON_ALPHA = "icon-alphabetical.png"
			PORN_TITLE = "Alphabitical listing of XXX Movies"
			PORN_SUMMARY = "Listings sorted by Alphabitical order of the XXX Movies database!"
			PORN_THUMB = R(ICON_ALPHA)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/xxx-all.html"
			oc.add(DirectoryObject(key=Callback(AlphabiticalPageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			#Add By Genre listing XXX Movie Page
			ICON_GENRE = "icon-genre.png"
			PORN_TITLE = "Genre listing of XXX Movies"
			PORN_SUMMARY = "Listings sorted by Genre of the XXX Movies database!"
			PORN_THUMB = R(ICON_GENRE)
			PORN_PAGE = "http://" + MOVIE2K_URL + "/genres-xxx.html"
			oc.add(DirectoryObject(key=Callback(GenrePageAdd, title=PORN_TITLE, page=PORN_PAGE, type=type, MOVIE2K_URL=MOVIE2K_URL), title=PORN_TITLE, summary=PORN_SUMMARY, thumb=PORN_THUMB))

			if Prefs['toppages'] == "Enabled":
				#Add Top XXX Movies
				Genre_Type = "Top XXX Movies"
				ICON_TOP = "icon-top.png"
				MOVIES_TITLE = "Top Movies"
				MOVIES_SUMMARY = "Your Top XXX Movies in the Movie2k database!"
				MOVIES_THUMB = R(ICON_TOP)
				MOVIES_PAGE = "http://" + MOVIE2K_URL + "/xxx-top.html"
				oc.add(DirectoryObject(key=Callback(MoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


#####################################################################################################
@route(PREFIX + '/DisabledScreen')
def DisabledScreen(title, MOVIE2K_URL):

	return ObjectContainer(header="We Apologize", message="This section has been disabled do to "+ MOVIE2K_URL +" disabling it on their site.")


#####################################################################################################
# This is special instructions for Roku users
@route(PREFIX + '/RokuUsersPasswordInput')
def RokuUsersPasswordInput(title):

	return ObjectContainer(header="Special Instructions for Roku Users", message="Inputting password, Roku users must be using version 2.6.7 or later of the Plex Roku Channel. If the Parantal Lock has been enabled, please input the password to view the adult content.  If the Parental Lock has been disabled enter the password to delete the password.  WARNING: DO NOT DIRECTLY TYPE OR PASTE THE TEXT IN THE INPUT CAPTCHA SECTION USING ROKU PLEX CHANNELS 2.6.4. THAT VERSION USES A SEARCH INSTEAD OF ENTRY SCREEN AND EVERY LETTER OF THE TEXT YOU ENTER WILL PRODUCE A SUBMIT FORM ON EACH LETTER.")


####################################################################################################
@route(PREFIX + '/AlphabiticalPageAdd')
def AlphabiticalPageAdd(title, page, type, MOVIE2K_URL):

	oc = ObjectContainer(title2=title)

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)

	Alpha_Type = "Numerical"
	ICON_MOVIES = "icon-numerical.png"
	MOVIES_TITLE = "Numerical"+" "+type
	MOVIES_SUMMARY = "Your Numerical list of the "+type+" database!"
	MOVIES_THUMB = R(ICON_MOVIES)

	oc.add(DirectoryObject(key=Callback(MovieGenres, title=MOVIES_TITLE, page=page, genre=Alpha_Type, thumb=MOVIES_THUMB, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
	if MOVIE2K_URL == "www.movie2k.tl":
		Page = HTML.ElementFromString(req.content).xpath('//div[@id="content"]/div')[0]
	elif MOVIE2K_URL == "www.movie2k.sx":
		Page = HTML.ElementFromString(req.content).xpath('//div[@id="content"]/div')[2]
	else:
		Page = HTML.ElementFromString(req.content).xpath('//div[@id="content"]/div[@id="content"]/div')[0]

	for AlphNumeric in Page.xpath('./div[@id="boxgrey"]'):
		Alpha_Type = AlphNumeric.xpath('./a')[0].text.strip()
		ICON_MOVIES = "icon-"+Alpha_Type.lower()+".png"
		MOVIES_TITLE = Alpha_Type+" "+type
		MOVIES_SUMMARY = "Your "+Alpha_Type+" list of the "+type+" database!"
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE_LINK = AlphNumeric.xpath('./a')[0].get('href')
		if MOVIE2K_URL == "www.movie2k.tl":
			MOVIES_PAGE = MOVIES_PAGE_LINK
		else:
			MOVIES_PAGE = "http://" + MOVIE2K_URL + MOVIES_PAGE_LINK

		oc.add(DirectoryObject(key=Callback(MovieGenres, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Alpha_Type, thumb=MOVIES_THUMB, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/GenrePageAdd')
def GenrePageAdd(title, page, type, MOVIE2K_URL):

	oc = ObjectContainer(title2=title)

	NotSkip = True
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)

	if MOVIE2K_URL == "www.movie2k.tl":
		elm = 'table[@id="tablemovies"]/tbody'
	elif MOVIE2K_URL == "www.movie2k.sx":
		elm = 'div[@id="maincontent4"]/table[@id="tablemoviesindex"]'
	else:
		elm = 'table[@id="tablemovies"]'

	for Genre in HTML.ElementFromString(req.content).xpath('//div[@id="content"]/'+elm+'/tr'):
		Genre_Type = Genre.xpath('./td[@id="tdmovies"]/a')[0].text
		ICON_MOVIES = "icon-"+Genre_Type.lower()+".png"
		MOVIES_TITLE = Genre_Type+" "+type
		MOVIES_SUMMARY = "Your "+Genre_Type+" "+type+" database!"
		MOVIES_THUMB = R(ICON_MOVIES)
		MOVIES_PAGE_PART = Genre.xpath('./td[@id="tdmovies"]/a')[0].get('href')
		MOVIES_PAGE = "http://" + MOVIE2K_URL + "/"+MOVIES_PAGE_PART

		if DisableAdult() != True and Genre_Type.lower() == 'adult':
			NotSkip = False

		if NotSkip:
			oc.add(DirectoryObject(key=Callback(MovieGenres, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=Genre_Type, thumb=MOVIES_THUMB, type=type, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=MOVIES_THUMB))
		else:
			NotSkip = True

	return oc


####################################################################################################
@route(PREFIX + '/MovieGenres')
def MovieGenres(title, page, genre, thumb, type, MOVIE2K_URL):
	
	oc = ObjectContainer(title2=title)

	i = 0
	num = 0
	SiteURL = "http://" + MOVIE2K_URL + "/"
	if MOVIE2K_URL == "www.movie2k.tl":
		if page.split('/')[3] == "movies-updates.html":
			elm = 'div[@class="pagidnation"]'
		else:
			elm = 'div[@id="maincontent4"]/div[@class="pagidnation"]'
		SiteURL = ""
	elif MOVIE2K_URL == "www.movie2k.sx":
		elm = 'div[@id="maincontent4"]/div[@id="pagination"]'
		num = -1
	else:
		elm = 'div[@id="maincontent4"]'

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)
	GenrePages = HTML.ElementFromString(req.content).xpath('//'+elm+'/div[@id="boxgrey"]')
	NUMPAGES = len(GenrePages) + num

	if NUMPAGES > 0:
		while i <= NUMPAGES:
			do = DirectoryObject()
			if i == 0:
				next_page = page
			else:
				next_page = SiteURL + GenrePages[i-1].xpath('./a')[0].get('href')
			i += 1
			do.title = "Page "+str(i)+" - List of "+genre+" "+type
			do.key = Callback(MoviePageAdd, title=do.title, page=next_page, genre=genre, type=type, MOVIE2K_URL=MOVIE2K_URL)
			do.summary = "Page "+str(i)+" of the line up of "+genre+" "+type+" from Movie2k."
			do.thumb = thumb
			oc.add(do)
	else:
		do = DirectoryObject()
		do.title = "Page 1 - List of "+genre+" "+type
		do.key = Callback(MoviePageAdd, title=do.title, page=page, genre=genre, type=type, MOVIE2K_URL=MOVIE2K_URL)
		do.summary = "Page 1 of the line up of "+genre+" "+type+" from Movie2k."
		do.thumb = thumb
		oc.add(do)

	return oc


####################################################################################################
@route(PREFIX + '/CinemaMoviePage')
def CinemaMoviePageAdd(title, page, type, MOVIE2K_URL):
	
	oc = ObjectContainer(title2=title)
	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	req = requests.get(page, headers=headers, cookies=cookies)
	CINEMA_MOVIE_PAGE = HTML.ElementFromString(req.content)
	SiteURL = ''
	dateadd = 'N/A'
	elm = ''

	if GetLanguage() == "German":
		MOVIES_LANG = "German"
	elif MOVIE2K_URL == "www.movie2k.tl":
		MOVIES_LANG = "German"
		elm = "/font"
	else:
		if MOVIE2K_URL == "www.movie2k.sx":
			SiteURL = "http://www.movie2k.sx"
		MOVIES_LANG = "English"

	for Movie in CINEMA_MOVIE_PAGE.xpath('//div[@id="maincontentnew"]/div'):
		try:	
			MOVIES_TD = Movie
			MOVIES_YEAR = time.strftime("%Y", time.localtime(time.time()))
			MOVIES_TITLE = MOVIES_TD.xpath("."+elm+"/a/img")[0].get('title').replace(' kostenlos','')
			MOVIES_PAGE = MOVIES_TD.xpath("."+elm+"/a")[0].get('href')
			MOVIES_THUMB = SiteURL + MOVIES_TD.xpath("."+elm+"/a/img")[0].get('src')
			MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the Cinema Movies line up on Movie2k."

			oc.add(DirectoryObject(key=Callback(SubGroupMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type, summary=MOVIES_SUMMARY, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))			
		except:
			pass

	for Movie in CINEMA_MOVIE_PAGE.xpath('//div[@id="maincontentnew"]/div'):
		try:	
			MOVIES_TD = Movie.xpath('./div')[0]
			MOVIES_YEAR = 'N/A'
			MOVIES_TITLE = MOVIES_TD.xpath("."+elm+"/a/img")[0].get('title').replace(' kostenlos','')
			MOVIES_PAGE = MOVIES_TD.xpath("."+elm+"/a")[0].get('href')
			MOVIES_THUMB = SiteURL + MOVIES_TD.xpath("."+elm+"/a/img")[0].get('src')
			MOVIES_SUMMARY = "Year: "+MOVIES_YEAR+" | Lang: "+MOVIES_LANG+" | Part of the Older Cinema Movies line up on Movie2k."

			oc.add(DirectoryObject(key=Callback(SubGroupMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type, summary=MOVIES_SUMMARY, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		except:
			pass

	return oc


####################################################################################################
@route(PREFIX + '/FeaturedMoviePageAdd')
def FeaturedMoviePageAdd(title, page, type, MOVIE2K_URL):

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

			oc.add(DirectoryObject(key=Callback(SubGroupMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type, summary=MOVIES_SUMMARY, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		i += 1

	return oc


####################################################################################################
@route(PREFIX + '/MovieGenrePage')
def MoviePageAdd(title, page, genre, type, MOVIE2K_URL):
	
	oc = ObjectContainer(title2=title)

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": MOVIE2K_URL, "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	if MOVIE2K_URL == "www.movie2k.tl":
		elm = "/tbody"
	else:
		elm = ""

	req = requests.get(page, headers=headers, cookies=cookies)
	GENRE_MOVIE_PAGE = HTML.ElementFromString(req.content)

	try:
		if MOVIE2K_URL == "www.movie2k.tl":
			GET_THUMB = GENRE_MOVIE_PAGE.xpath('//body/script')
		elif MOVIE2K_URL == "www.movie2k.sx":
			GET_THUMB = GENRE_MOVIE_PAGE.xpath('//table[@id="tablemoviesindex"]/script')
		else:
			GET_THUMB = GENRE_MOVIE_PAGE.xpath('//div[@id="maincontent4"]/script')
	except:
		GET_THUMB = None

	i = 0
	for Movie in GENRE_MOVIE_PAGE.xpath('//div[@id="maincontent4"]/table[@id="tablemoviesindex"]'+elm+'/tr'):
		MOVIES_TD = Movie.xpath('./td[@id="tdmovies"]')
		MOVIES_TITLE = re.sub('\t\r\0', '', MOVIES_TD[0].xpath("./a")[0].text).replace('     ', '').replace(',', ', ').replace(':', ': ')
		if type == 'TV Shows':
			dateadd = MOVIES_TD[3].text
			if dateadd == None:
				dateadd = 'N/A'
		else:
			dateadd = 'N/A'
		try:
			try:
				MOVIES_YEAR = MOVIES_TD[1].xpath("./div")[7].text
			except:
				MOVIES_YEAR = re.sub('[^0-9]', '', MOVIES_TD[2].text)
			if MOVIES_YEAR == None or MOVIES_YEAR == "":
				try:
					MOVIES_YEAR = re.sub('[^0-9]', '', MOVIES_TD[4].text)
				except:
					pass
			if MOVIES_YEAR == None or MOVIES_YEAR == "":
				MOVIES_YEAR = "N/A"
		except:
			MOVIES_YEAR = "N/A"
		
		if MOVIE2K_URL == "www.movie2k.sx":
			try:
				MOVIES_LANG = MOVIES_TD[3].text.capitalize()
			except:
				MOVIES_LANG = "N/A"
		else:
			try:
				try:
					LANGUAGE_URL = MOVIES_TD[4].xpath("./img")[0].get('src')
				except:
					LANGUAGE_URL = MOVIES_TD[5].xpath("./img")[0].get('src')
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
			if MOVIE2K_URL == "www.movie2k.sx":
				jj = i
				SiteURL = "http://www.movie2k.sx"
			else:
				jj = 0
				SiteURL = ""
			MOVIES_THUMB = SiteURL + GET_THUMB[jj].text.split(Movie.get('id'))[1].split("img src='")[1].split("'")[0]
		except:
			MOVIES_THUMB = None

		if MOVIES_LANG == GetLanguage() or MOVIES_LANG == 'N/A' or GetLanguage() == 'All':
			if MOVIE2K_URL == 'www.movie2k.sx' and type == 'TV Shows':
				oc.add(DirectoryObject(key=Callback(TVShowSeasons, title=MOVIES_TITLE, page=MOVIES_PAGE, genre=genre, type=type, MOVIE2K_URL=MOVIE2K_URL, thumb=MOVIES_THUMB, MOVIES_LANG=MOVIES_LANG), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
			else:
				oc.add(DirectoryObject(key=Callback(SubGroupMoviePageAdd, title=MOVIES_TITLE, page=MOVIES_PAGE, date=MOVIES_YEAR, dateadd=dateadd, thumbck=MOVIES_THUMB, type=type, summary=MOVIES_SUMMARY, MOVIE2K_URL=MOVIE2K_URL), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=MOVIES_THUMB)))
		i += 1

	if len(oc) < 1:
		oc = ObjectContainer(header="We Apologize", message=title + " does not have any listings for processing.  Try again later to see if Movie2k site adds any listings.")

	return oc


####################################################################################################
@route(PREFIX + '/TVandMovieGroupPage')
def SubGroupMoviePageAdd(title, page, date, dateadd, thumbck, type, summary, MOVIE2K_URL, CSRF_TOKEN=None):

	title = unicode(title, errors='replace')
	oc = ObjectContainer(title2=title)

	if CSRF_TOKEN != None:
		cookies = Dict['_movie2k_uid']
		headers = {"Accept": "text/javascript, application/javascript", "Referer": "http://"+MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum], "X-CSRF-Token": CSRF_TOKEN, "X-Requested-With": "XMLHttpReques"}
		req = requests.get(page, headers=headers, cookies=cookies)
		page = "http://www.movie2k.sx" + req.content.split("'")[1]
	
	# List Host Sites for Playback
	summary = summary.split(" | ")[0] + " | " + summary.split(" | ")[1] + " | List the Host Sites from Movie2k."
	oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=title, page=page, date=date, dateadd=dateadd, thumbck=thumbck, type=type, MOVIE2K_URL=MOVIE2K_URL), title=title, summary=summary, thumb=Callback(GetThumb, url=thumbck)))

	# Add Favorite Movie4k.to link
	ICON_ADDFAVORITE = "icon-add-favorite.png"
	ADDFAVORITE_THUMB = R(ICON_ADDFAVORITE)
	summary = "Add \""+title+"\" as a favorite link from Movie2k!"
	ADDFAVORITE_TITLE = "Add to My Favorite Links"
	if page.split('/')[0] != "http:":
		page = "http://"+MOVIE2K_URL+"/"+page
	oc.add(DirectoryObject(key=Callback(InputFavoriteURL, title=ADDFAVORITE_TITLE, MOVIE2K_URL=MOVIE2K_URL, query=page), title=ADDFAVORITE_TITLE, summary=summary, thumb=ADDFAVORITE_THUMB))

	# Add Watchit Later Video Movie4k.to link
	if HostVideoDownload.stop == None:
		HostVideoDownload.stop = CheckForDownload()
	ICON_ADDWATCHITLATER = "icon-add-watchit-later.png"
	WATCHIT_THUMB = R(ICON_ADDWATCHITLATER)
	summary = "Add \""+title+"\" as a watchit later video download from a Movie2k Host!"
	WATCHIT_TITLE = "Add to My Watchit Later Videos"
	oc.add(DirectoryObject(key=Callback(SubMoviePageAdd, title=title, page=page, date=date, dateadd=dateadd, thumbck=thumbck, type=type, MOVIE2K_URL=MOVIE2K_URL, watchitlater=True), title=WATCHIT_TITLE, summary=summary, thumb=WATCHIT_THUMB))

	return oc


####################################################################################################
@route(PREFIX + '/TVandMovieHostPage')
def SubMoviePageAdd(title, page, date, dateadd, thumbck, type, MOVIE2K_URL, watchitlater=False):

	if watchitlater == "True":
		host_count = 1
	else:
		host_count = int(Prefs['host_count'])

	if host_count != 1:
		pl = "s"
	else:
		pl = ""

	title = unicode(title, errors='replace')
	oc = ObjectContainer(title2=title+" - ["+str(host_count)+" HOST"+pl+" per Page]")

	if page.split('/')[0] != "http:":
		CURRENT_MOVIE2K_URL = MOVIE2K_URL
		page = "http://"+MOVIE2K_URL+"/"+page
	else:
		CURRENT_MOVIE2K_URL = page.split('/')[2]

	cookies = Dict['_movie2k_uid']
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": CURRENT_MOVIE2K_URL, "Referer": "http://"+CURRENT_MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
	
	req = requests.get(page, headers=headers, cookies=cookies)
	MOVIE_PAGE_HTML = HTML.ElementFromString(req.content)

	if thumbck == "" or thumbck == None or thumbck.split('/')[4] == "noposter.gif" or thumbck.split('/')[4] == "comingsoon.jpg":
		GET_THUMB = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')[0]
		thumb = GET_THUMB.xpath('./a/img')[0].get('src')
		if thumb.split('/')[0] != "http:":
			thumb = "http://"+CURRENT_MOVIE2K_URL+"/"+thumb
	else:
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

	p = (float(NumHostListing1)+float(NumHostListing2))/float(host_count) - (NumHostListing1+NumHostListing2)/host_count
	jj = (NumHostListing1+NumHostListing2)/host_count
	if p > 0:
		jj += 1

	if jj == 0:
		try:
			Host = GetHost(url=page, HostPageInfo=MOVIE_PAGE_HTML)
			if type == "Movies":
				Quality = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]//span/span/img')[0].get('title').split(' ')[2].capitalize()
				Hosts =  "%s | Quality: %s" % (Host, Quality)
			else:
					Hosts = Hosts + Host

			MOVIES_SUMMARY = "Page - " + str(i) + " | Host: " + Hosts
			MOVIES_TITLE = title
			if Prefs['swaptitle'] == "Enabled":
				MOVIES_SUMMARY = title
				MOVIES_TITLE = str(i) + ": " + Hosts
			if Host == "Urmediazone":
				oc = ObjectContainer(header="We Apologize", message=title + " does not have any Host sites listed for video playback.  Try again later to see if Movie2k site adds any Hosts.")
			else:
				oc.add(DirectoryObject(key=Callback(TheMovieListings, title=title, page=page, date=date, dateadd=dateadd, thumb=thumb, type=type, PageOfHosts=0, MOVIE2K_URL=MOVIE2K_URL, Host=Host, watchitlater=watchitlater), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=thumb)))
		except:
			pass
	else:
		while i <= jj:
			while HostCount <= host_count:
				if Num1 < NumHostListing1:
					try:
						Host = Listing[Num1].xpath("./td/a/img")[0].get('title').split(' ')[0].partition('.')[0].capitalize()
						if type == "Movies":
							try:
								Quality = Listing[Num1].xpath("./td/img")[0].get('title').split(' ')[2]
							except:
								Quality = "N/A"
					except:
						if MOVIE2K_URL == "www.movie2k.sx":
							Host = Listing[Num1].xpath("./td/a")[2].text.partition('.')[0].capitalize()
							if type == "Movies":
								try:
									Quality = Listing[Num1].xpath("./td/img")[0].get('title').split(' ')[2].capitalize()
								except:
									Quality = "N/A"
					if Host == None or Host == "":
						Host = GetHost(HostPageInfo=MOVIE_PAGE_HTML)
						if type == "Movies":
							try:
								Quality = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]//span/span/img')[0].get('title').split(' ')[2].capitalize()
							except:
								Quality = "N/A"
					Num1 += 1
				elif Num2 < NumHostListing2:
					ScriptListing = StringListing[k].text.split('links[')
					NumHosts = len(ScriptListing) - 2	
					Host = ScriptListing[sll].split('title=\\"')[1].split('\\"')[0].split(' ')[0].partition('.')[0].capitalize()
					#if type == "Movies":
					#	Quality = ScriptListing[sll].split('title=\\"')[2].split('\\"')[0].split(' ')[2]
					if sll == NumHosts:
						k += 1
						sll = 1
					else:
						sll += 1
					Num2 += 1
				else:
					HostCount = host_count
				HostCount += 1

				if host_count == 1 and type == "Movies":
					Hosts =  "%s | Quality: %s, " % (Host, Quality)
				else:
					Hosts = Hosts + Host + ", "

			MOVIES_SUMMARY = "Page - " + str(i) + " | Host"+pl+": " + Hosts[:-2]
			MOVIES_TITLE = title
			if Prefs['swaptitle'] == "Enabled":
				MOVIES_SUMMARY = title
				MOVIES_TITLE = str(i) + ": " + Hosts[:-2]
			oc.add(DirectoryObject(key=Callback(TheMovieListings, title=title, page=page, date=date, dateadd=dateadd, thumb=thumb, type=type, PageOfHosts=i, MOVIE2K_URL=MOVIE2K_URL, watchitlater=watchitlater), title=MOVIES_TITLE, summary=MOVIES_SUMMARY, thumb=Callback(GetThumb, url=thumb)))
			HostCount = 1
			Hosts = ""
			i += 1

	if len(oc) < 1:
		oc = ObjectContainer(header="We Apologize", message=title + " does not have any Host sites listed for video playback.  Try again later to see if Movie2k site adds any Hosts.")

	return oc


####################################################################################################
@route(PREFIX + '/TVandTheMovieListings')
def TheMovieListings(title, page, date, dateadd, thumb, type, PageOfHosts, MOVIE2K_URL, Host=None, watchitlater=False):

	title = unicode(title, errors='replace')
	oc = ObjectContainer(title2=title+" - [HOST VIDEO INFO]")

	global GoodLink

	@parallelize
	def GetMovieList(title=title, page=page, date=date, dateadd=dateadd, thumb=thumb, type=type, PageOfHosts=PageOfHosts, Host=Host, watchitlater=watchitlater):

		if page.split('/')[0] != "http:":
			CURRENT_MOVIE2K_URL = MOVIE2K_URL
			page = "http://"+MOVIE2K_URL+"/"+page
		else:
			CURRENT_MOVIE2K_URL = page.split('/')[2]

		cookies = Dict['_movie2k_uid']
		headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "en-US,en;q=0.8", "Connection": "keep-alive", "Host": CURRENT_MOVIE2K_URL, "Referer": "http://"+CURRENT_MOVIE2K_URL, "User-Agent": UserAgent[UserAgentNum]}
		req = requests.get(page, headers=headers, cookies=cookies)

		MOVIE_PAGE_HTML = HTML.ElementFromString(req.content)

		MOVIE_INFO = MOVIE_PAGE_HTML.xpath('//div[@id="details"]')[0].text_content()
		source_title = "Movie2k"

		summary = MOVIE_PAGE_HTML.xpath('//div[@class="moviedescription"]')[0].text
		if summary == None or summary == "":
			summary = "Description not given..."

		try:
			rating = float(MOVIE_PAGE_HTML.xpath('//div[@id="details"]/a')[0].text)
		except:
			rating = 0.0

		if date == "N/A":
			try:
				date = re.sub('[^0-9]', '', MOVIE_INFO.split('Year:')[1])
				if date == "":
					date =  "0001"
			except:
				date = re.sub('[^0-9]', '', MOVIE_INFO.split('Land/Jahr:')[1])
				if date == "":
					date =  "0001"

		date = Datetime.ParseDate(date[:4], "%Y")

		genres = []
		genre = MOVIE_INFO.split('Genre:')[1].split('|')[0]
		genres = StripArray(arraystrings=genre.split(','))

		try:
			try:
				duration = int(float(re.sub('[^0-9]', '', MOVIE_INFO.split('Length:')[1].split('min')[0]))*60*1000)
			except:
				duration = int(float(re.sub('[^0-9]', '', MOVIE_INFO.split('nge:')[1].split('Min')[0]))*60*1000)
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
			actors = 'Actors Not Available'
			guest_stars.append(actors)

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
				else:
					content_rating = 'NR'
			except:
				content_rating = 'NR'

		try:
			subtitle = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')[1]
			try:
				try:
					season = int(subtitle.xpath('./span/h1/a/span')[0].text.split('Season ')[1].split(',')[0].replace(' ', ''))
					index = int(subtitle.xpath('./span/h1/a/span')[0].text.split('Episode ')[1].replace(' ', ''))
				except:
					season = int(subtitle.xpath('./h1/span/a')[0].text.split('Season ')[1].split(',')[0].replace(' ', ''))
					index = int(subtitle.xpath('./h1/span/a')[0].text.split('Episode ')[1].replace(' ', ''))
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

		if watchitlater == "True":
			host_count = 1
		else:
			host_count = int(Prefs['host_count'])

		Listing = MOVIE_PAGE_HTML.xpath('//div[@id="menu"]//tr[@id="tablemoviesindex2"]')
		StringListing = MOVIE_PAGE_HTML.xpath('//div[@id="menu"]//script[@type="text/javascript"]')
		NumHostListing1 = len(Listing)
		NumStringListing = len(StringListing)
		NumHostListing2 = 0
		nsl = 0
		out = {'CreatePage': True, 'CurrentPage': 1, 'HostCountTotal': 1, 'sll': 1, 'k': 0}

		while nsl < NumStringListing:
			NumHosts = len(StringListing[nsl].text.split('links[')) - 2
			NumHostListing2 = NumHostListing2 + NumHosts
			nsl += 1

		p = (float(NumHostListing1)+float(NumHostListing2))/float(host_count) - (NumHostListing1+NumHostListing2)/host_count
		NumPages = (NumHostListing1+NumHostListing2)/host_count
		if p > 0:
			NumPages += 1

		TotalHosts = NumHostListing1 + NumHostListing2
		if TotalHosts == 0:
			TotalHosts = 1

		Log("Listing Length: "+str(NumHostListing1))
		Log("Listing Script Length: "+str(NumStringListing))
		Log("Number of Pages: "+str(NumPages))
		Log("Total Hosts: "+str(TotalHosts))
		Log("Page of Hosts: "+str(PageOfHosts))

		for num in range(0,TotalHosts):
			if int(PageOfHosts) != 0:
				num2 = num - NumHostListing1
				if num < NumHostListing1:
					try:
						Host = Listing[num].xpath("./td/a/img")[0].get('title').split(' ')[0].partition('.')[0].capitalize()
					except:
						if MOVIE2K_URL == "www.movie2k.sx":
							Host = Listing[num].xpath("./td/a")[2].text.partition('.')[0].capitalize()
					if Host == None or Host == "":
						Host = GetHost(url=page, HostPageInfo=MOVIE_PAGE_HTML)
					MOVIE_PAGE = Listing[num].xpath("./td/a")[0].get('href')
					if MOVIE_PAGE.split('/')[0] != "http:":
						MOVIE_PAGE = "http://" + CURRENT_MOVIE2K_URL + "/" + MOVIE_PAGE
					if type == 'TV Shows':
						DateAdded = dateadd
						Quality = "DVDRip/BDRip"
					else:
						DateAdded = Listing[num].xpath("./td/a")[0].text
						Quality = Listing[num].xpath("./td/img")[0].get('title').split(' ')[2]
				elif num2 < NumHostListing2:
					ScriptListing = StringListing[out['k']].text.split('links[')
					NumHosts = len(ScriptListing) - 2	
					Host = ScriptListing[out['sll']].split('title=\\"')[1].split('\\"')[0].split(' ')[0].partition('.')[0].capitalize()
					MOVIE_PAGE = ScriptListing[out['sll']].split('href=\\"')[1].split('\\"')[0]
					if MOVIE_PAGE.split('/')[0] != "http:":
						MOVIE_PAGE = "http://" + CURRENT_MOVIE2K_URL + "/" + MOVIE_PAGE
					if type == 'TV Shows':
						DateAdded = dateadd
						Quality = "DVDRip/BDRip"
					else:
						DateAdded = ScriptListing[out['sll']].split('href=\\"')[1].split('\\">')[1].split(' <')[0]
						Quality = ScriptListing[out['sll']].split('title=\\"')[2].split('\\"')[0].split(' ')[2]

					if out['sll'] == NumHosts:
						out['k'] = out['k'] + 1
						out['sll'] = 1
					else:
						out['sll'] = out['sll'] + 1
			else:
				MOVIE_PAGE = page
				out['CurrentPage'] = 0
				DateAdded = dateadd
				if type == 'TV Shows':
					Quality = "DVDRip/BDRip"
				else:
					QualitySub = MOVIE_PAGE_HTML.xpath('//div[@id="maincontent5"]/div/div')[1]
					Quality = QualitySub.xpath("./span/span/img")[0].get('title').split(' ')[2]

			@task
			def GetMovieObjects(Host=Host, MOVIE_PAGE=MOVIE_PAGE, DateAdded=DateAdded, Quality=Quality, CreatePage=out['CreatePage'], CurrentPage=out['CurrentPage'], watchitlater=watchitlater):

				global GoodLink

				if CreatePage:
					if CurrentPage == int(PageOfHosts):
						if Host == 'N/a' or Host == 'Divx' or Host == 'DivX Hoster' or Host == 'Flash' or Host == 'Flash Hoster' or Host == 'Embed':
							Host = GetHost(Host=Host, url=MOVIE_PAGE)

						show = "ADDED: "+ DateAdded + " | HOST: " + Host + " | QUALITY: " + Quality
						show_title = title
						if Prefs['swaptitle'] == "Enabled":
							show = title
							show_title = "QUALITY: " + Quality +" | HOST: " + Host + " | ADDED: " + DateAdded

						url = MOVIE_PAGE+"?title="+String.Quote(title, usePlus=True)+"&summary="+String.Quote(summary.strip(), usePlus=True)+"&show="+String.Quote(show, usePlus=True)+"&date="+String.Quote(str(date), usePlus=True)+"&thumb="+String.Quote(thumb, usePlus=True)+"&host="+Host+"&season="+str(season)+"&index="+str(index)+"&type="+String.Quote(type, usePlus=True)+"&genres="+String.Quote(genre, usePlus=True)+"&director="+String.Quote(director, usePlus=True)+"&actors="+String.Quote(actors, usePlus=True)+"&duration="+str(duration)+"&rating="+str(rating)+"&content_rating="+content_rating

						if Host == '180upload' or Host == 'Clicktoview' or Host == 'Fileloby' or Host == 'Grifthost' or Host == 'Lemuploads' or Host == 'Megarelease' or Host == 'Vidbux' or Host == 'Vidplay' or Host == 'Vidxden':
							show_update = "Click here if you want OCR to try and decode Captcha text."
							show_title = show_title +  " - [USES CAPTCHA]"
							oc.add(DirectoryObject(key=Callback(CaptchaSection, title=title, page=page, date=date, thumb=thumb, type=type, summary=summary.strip(), directors=directors, guest_stars=guest_stars, genres=genres, duration=duration, rating=float(rating), season=season, index=index, show=show_update, content_rating=content_rating, source_title=source_title, url=url, Host=Host), title=show_title, thumb=Callback(GetThumb, url=thumb), summary=show))
						elif watchitlater == "True":
							(HostVideoDownload.MyDownloadPath, HostVideoDownload.MyDownloadRequest, GoodLink) = GetHostVideo(title=title, date=String.Quote(str(date), usePlus=True), DateAdded=String.Quote(str(DateAdded), usePlus=True), Quality=Quality, thumb=String.Quote(thumb, usePlus=True), type=String.Quote(type, usePlus=True), summary=String.Quote(summary.strip(), usePlus=True), directors=String.Quote(director, usePlus=True), guest_stars=String.Quote(actors, usePlus=True), genres=String.Quote(genre, usePlus=True), duration=str(duration), rating=str(rating), season=str(season), index=str(index), content_rating=content_rating, source_title=source_title, url=MOVIE_PAGE, Host=Host)
						else:
							if type == 'TV Shows':
								oc.add(EpisodeObject(
										url = url,
										title = show_title,
										summary = summary.strip(),
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
										title = show_title,
										summary = summary.strip(),
										directors = directors,
										genres = genres,
										duration = duration,
										rating = rating,
										content_rating = content_rating,
										source_title = show,
										originally_available_at = date,
										thumb = Callback(GetThumb, url=thumb)))

			if (num+1)%host_count == 0:
				if out['CurrentPage'] == int(PageOfHosts):
					out['CreatePage'] = False
				else:
					out['CurrentPage'] = out['CurrentPage'] + 1

			if out['HostCountTotal'] == TotalHosts:
				out['CreatePage'] = False
			else:
				out['HostCountTotal'] = out['HostCountTotal'] + 1

	if GoodLink != None:
		if GoodLink == True:
			oc = ObjectContainer(header="Download Started", message="Please DO NOT shut down or restart Plex Media Server at this time or download will fail.  Go to Watchit Later to check on the status.")
		else:
			oc = ObjectContainer(header="We Apologize", message="There was a problem with the Host video.  Host video errored do to "+GoodLink+".  Please try again by clicking the OK button, choose another Host.")
		GoodLink = None
	elif len(oc) < 1:
		oc = ObjectContainer(header="We Apologize", message="An error has occured processing Host site information.  Please try again.")

	return oc


####################################################################################################
def run_proxifier():
	global PROXIFIER_PROCESS

	try:
		Log("1 - I am here now!!!!!")
		Log(PROXIFIER_PROCESS)
		stdout = PROXIFIER_PROCESS.stdout.read()
		stderr = PROXIFIER_PROCESS.stderr.read()
		Log(stdout)
		Log(stderr)
		Log("2 - I am here now!!!!!")
	except:
		pass

	cmd = "C:\\Program Files\\Proxifier\\Proxifier.exe"
	PROXIFIER_PROCESS = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	code = PROXIFIER_PROCESS.wait()

	#PROXIFIER_PROCESS.terminate()
	stdoutdata, stderrdata = PROXIFIER_PROCESS.communicate()

	return code


#####################################################################################################
# This is the section for Host sites using Captcha
@route(PREFIX + '/CaptchaSection')
def CaptchaSection(title, page, date, thumb, type, summary, directors, guest_stars, genres, duration, rating, season, index, show, content_rating, source_title, url, Host):

	oc = ObjectContainer(title2=title)

	ICON_INSTRUCTIONS = "icon-instructions.png"
	INSTRUCTIONS_THUMB = R(ICON_INSTRUCTIONS)
	date = Datetime.ParseDate(date, "%Y")
	directors = [directors]
	guest_stars = [guest_stars]
	genres = [genres]
	duration = int(duration)
	rating = float(rating)
	season = int(season)
	index = int(index)
	title = title

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
@route(PREFIX + '/CaptchaInput')
def CaptchaInput(title, page, date, thumb, type, summary, directors, guest_stars, genres, duration, rating, season, index, content_rating, source_title, url, Host, query):

	oc = ObjectContainer(title2=title)

	show = "Host: " + Host + " - Captcha has been processed"
	hosts = LoadData(fp=CAPTCHA_DATA)
	date = Datetime.ParseDate(date, "%Y")
	directors = [directors]
	guest_stars = [guest_stars]
	genres = [genres]
	duration = int(duration)
	rating = float(rating)
	season = int(season)
	index = int(index)

	i = 1
	for gethost in hosts:
		if gethost[i]['host'] == Host:
			gethost[i]['response'] = query.replace('\n', '')
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
@route(PREFIX + '/RokuUsers')
def RokuUsers(title):

	return ObjectContainer(header="Special Instructions for Roku Users", message="To enter Captcha text, Roku users must be using version 2.6.7 or later of the Plex Roku Channel. You can choose to type in the Captcha image text or allow the OCR to try and deocode it. However, the OCR decode rate is very low.  WARNING: DO NOT DIRECTLY TYPE OR PASTE THE TEXT IN THE INPUT CAPTCHA SECTION USING ROKU PLEX CHANNELS 2.6.4. THAT VERSION USES A SEARCH INSTEAD OF ENTRY SCREEN AND EVERY LETTER OF THE TEXT YOU ENTER WILL PRODUCE A SUBMIT FORM ON EACH CAPTCHA LETTER.")


####################################################################################################
def strip_one_space(s):

	if s.endswith(" "): s = s[:-1]
	if s.startswith(" "): s = s[1:]

	return s


####################################################################################################
def GetHost(Host=None, url=None, HostPageInfo=None):

	#
	#Check for Real Video Hoster if set to N/A or DivX Hoster or Flash Hoster is set
	#
	(HostPage, LinkType) = GetHostPageURL(Host=Host, url=url, HostPageInfo=HostPageInfo)
	Host = HostPage.split('http://')[1].split('.')[0].capitalize()
	if Host == 'Www' or Host == 'Embed' or Host == 'Beta' or Host == 'Movie':
		Host = HostPage.split('http://')[1].split('.')[1].capitalize()

	return Host


####################################################################################################
def GetLang(lang):
	if lang == "us_flag_small":
		r = "English"
	elif lang == "us_ger_small" or lang == "DE":
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
@route(PREFIX + '/GetThumb')
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
			response = requests.get(url, headers=headers)
			imgData = response.content

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
	cookies = CookieDict(cookies=session.cookies)
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
		oc = ObjectContainer(header="We Apologize", message="This Trailer Search did not contain any videos")

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