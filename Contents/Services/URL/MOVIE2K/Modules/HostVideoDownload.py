####################################################################################################
# Setting up imports

import os
import sys
import time
import re
from threading import Thread
from HostSites import GetMovie
from HostServices import GetHostPageURL
from HostServices import LoadData
from HostServices import JsonWrite

try:
	path = os.getcwd().split("?\\")[1].split('Plug-in Support')[0]+"Plug-ins\MOVIE2K.bundle\Contents\Services\URL\MOVIE2K\Modules"
except:
	path = os.getcwd().split("Plug-in Support")[0]+"Plug-ins/MOVIE2K.bundle/Contents/Services/URL/MOVIE2K/Modules"
sys.path.append(path)

try:
	import requests
except:
	import requests25 as requests

ContentLength = None
NoError = None
threadList = []


def downloads(VideoStreamLink, path, startByte=0, endByte=None):
	global ContentLength
	global NoError

	Log("DOWNLOAD URL: "+VideoStreamLink)
	headers = {'User-Agent': UserAgent, 'Connection': 'keep-alive'}

	if startByte != 0:
		headers['Range'] = 'bytes=%d-%d' % (startByte,endByte)

	request = requests.get(VideoStreamLink, headers=headers, stream=True, allow_redirects=True)
	Log("####################################################################################################")
	Log(request.headers)
	Log("####################################################################################################")
	Log("STATUS CODE: "+str(request.status_code))
	Log("####################################################################################################")
	if str(request.status_code) == "416":
		Log("Thread didn't get the file it was expecting. Retrying...")
		time.sleep(5)
		return downloads(VideoStreamLink, path, startByte, endByte)
	elif str(request.status_code) == "403":
		NoError = "Wrong IP was returned"
		ContentLength = -1
		return
	try:
		ContentLength = int(request.headers['Content-Length'].strip())
	except:
		ContentLength = -1
	Log("GET CONTENT-LENGTH IN DOWNLOADS: "+str(ContentLength))

	if not os.path.exists(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))

	with open(path, 'wb') as handle:
		for chunk in request.iter_content(chunk_size=1024):
       			if not chunk: # filter out keep-alive new chunks
				break
			handle.write(chunk)

	handle.close()

def MyDownload(title, VideoStreamLink, path=None):
	global threadList

	if path != None:
		startByte = os.stat(path).st_size
	else:
		path = "Videos\%s_%s.%s" % (re.sub('\W', '_', title, flags=re.UNICODE), str(time.time()), VideoStreamLink.split('/')[-1].split('.')[1].partition('?')[0])
		startByte = 0

	thread = Thread(target=downloads, args=(VideoStreamLink, path, startByte,))
	#thread.setDaemon(True)
	thread.start()
	threadList.append(thread)

	for myThreads in threadList:
		myThreads.join()

	Log('Thread is not alive: ' + str(thread.is_alive()))

	return path


####################################################################################################
def GetHostVideo(title, date, DateAdded, Quality, thumb, type, summary, directors, guest_stars, genres, duration, rating, season, index, content_rating, source_title, url, Host):
	global ContentLength
	global NoError
	WATCHIT_DATA = "watchit.data.json"

	(HostPage, LinkType) = GetHostPageURL(Host=Host, url=url)

	#Check For Real Host
	Host = HostPage.split('http://')[1].split('.')[0].capitalize()
	if Host == 'Www' or Host == 'Embed' or Host == 'Beta' or Host == 'Movie':
		Host = HostPage.split('http://')[1].split('.')[1].capitalize()

	VideoStreamLink = GetMovie(Host=Host, HostPage=HostPage, url=url, LinkType=LinkType)
	if "Wrong_IP" in VideoStreamLink:
		NoError = "Wrong IP was returned"
	elif "Host_Down" in VideoStreamLink:
		NoError = "Host Down was returned"
	elif "Video_Removed" in VideoStreamLink:
		NoError = "Video Removed was returned"
	elif "Geolocation_Lockout" in VideoStreamLink:
		NoError = "Geolocation Lockout was returned"
	else:
		NoError = True
		path = MyDownload(title=title, VideoStreamLink=VideoStreamLink)
		Log("Get Conntent Length: "+str(ContentLength))

		if int(ContentLength) == 8 and NoError == True:
			NoError = "failed to start downloading"

			if os.path.isfile(path):
				os.remove(path)
			else:
				Log("Error: %s file not found" % path)
		elif NoError == True:
			videotype = path.split('/')[-1].split('.')[1]

			hosts = LoadData(fp=WATCHIT_DATA, GetJson=3)
			numHosts = len(hosts)
			i = 1
			jj = 0
			while jj <= numHosts:
				try:
					if hosts[jj][i]['Path'] == "":
						hosts[jj][i]['Type'] = type
						hosts[jj][i]['DateAdded'] = DateAdded
						hosts[jj][i]['Quality'] = Quality
						hosts[jj][i]['Path'] = path
						hosts[jj][i]['Host'] = Host
						hosts[jj][i]['Title'] = title
						hosts[jj][i]['Summary'] = summary
						hosts[jj][i]['Genres'] = genres
						hosts[jj][i]['Directors'] = directors
						hosts[jj][i]['GuestStars'] = guest_stars
						hosts[jj][i]['Duration'] = duration
						hosts[jj][i]['Rating'] = rating
						hosts[jj][i]['Index'] = index
						hosts[jj][i]['Season'] = season
						hosts[jj][i]['ContentRating'] = content_rating
						hosts[jj][i]['SourceTitle'] = source_title
						hosts[jj][i]['Date'] = date
						hosts[jj][i]['ThumbURL'] = thumb
						hosts[jj][i]['VideoType'] = videotype
						hosts[jj][i]['VideoStreamLink'] = VideoStreamLink
						hosts[jj][i]['ContentLength'] = ContentLength
					else:
						i += 1
						jj += 1
				except:
					hosts.append({i : {'Type': type, 'Path': path, 'Host': Host, 'DateAdded': DateAdded, 'Quality': Quality, 'ThumbURL': thumb, 'Title': title, 'Summary':summary, 'Genres': genres, 'Directors': directors, 'GuestStars':guest_stars, 'Duration': duration, 'Rating': rating, 'Index': index, 'Season': season, 'ContentRating': content_rating, 'SourceTitle': source_title, 'Date': date, 'VideoType': videotype, 'VideoStreamLink': VideoStreamLink, 'ContentLength': ContentLength}})
					break

			JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)

	return NoError