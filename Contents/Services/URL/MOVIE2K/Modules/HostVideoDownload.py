####################################################################################################
# Setting up imports

import os
import sys
import ast
import time
import re
import threading

from HostSites import GetMovie
from HostServices import GetHostPageURL
from HostServices import LoadData
from HostServices import JsonWrite

try:
	path = os.getcwd().split("?\\")[1].split('Plug-in Support')[0]+"Plug-ins\MOVIE2K.bundle\Contents\Services\URL\MOVIE2K\Modules"
	DownloadPath = '\\'
except:
	path = os.getcwd().split("Plug-in Support")[0]+"Plug-ins/MOVIE2K.bundle/Contents/Services/URL/MOVIE2K/Modules"
	DownloadPath = '/'
	
if path not in sys.path:
	sys.path.append(path)

try:
	import requests
except:
	import requests25 as requests


threadList        = []
ResumeParts       = []
ResumePath        = None
MyDownloadPath    = None
MyDownloadRequest = None
stopAutoResume    = None
stopAutoPatcher   = None
stopStitching     = None
stop              = None
isAwake           = False

WATCHIT_DATA      = "watchit.data.json"


####################################################################################################
def setInterval(interval):
	def decorator(function):
		def wrapper(*args, **kwargs):
			stopped = threading.Event()

			def loop(): # executed in another thread
				while not stopped.wait(interval): # until stopped
					function(*args, **kwargs)

			t = threading.Thread(target=loop)
			#t.daemon = True # stop if the program exits
			t.start()
			return stopped
		return wrapper
	return decorator


####################################################################################################
@setInterval(.5)
def CheckForDownload():
	global MyDownloadPath
	global MyDownloadRequest
	global stop

	if MyDownloadRequest != None:
		MyDownloadThread(MyDownloadPath, MyDownloadRequest)
		MyDownloadPath = None
		MyDownloadRequest = None
		stop.set() # stop the timer loop
		stop = None


####################################################################################################
@setInterval(.5)
def StitchFilesTogether():
	global ResumeParts
	global ResumePath
	global stopStitching

	if ResumePath != None:
		combine_files(parts=ResumeParts, path=ResumePath)
		ResumeParts = []
		ResumePath = None
		stopStitching.set() # stop the timer loop
		stopStitching = None
		
####################################################################################################
@setInterval(10)
def CheckforRuntimeUpdate():
	if sys.platform.startswith('win'):
		runtime = Core.storage.join_path(Core.app_support_path, Core.config.bundles_dir_name) + "\Framework.bundle\Contents\Resources\Versions\\2\Python\Framework\components\\runtime.py"
		LocalFrameworkPath = Core.storage.join_path(Core.app_support_path, Core.config.bundles_dir_name) + "\Framework.bundle\Contents\Resources\Versions\\2\Python\Framework\components"
		docutils = os.environ['PYTHONPATH'].split('DLLs')[0] + "Resources\Plug-ins\Framework.bundle\Contents\Resources\Versions\\2\Python\Framework\docutils.py"
		AppFramworkPath = os.environ['PYTHONPATH'].split('DLLs')[0] + "Resources\Plug-ins\Framework.bundle\Contents\Resources\Versions\\2\Python\Framework"
		runtimePatchedFile = Core.storage.join_path(Core.app_support_path, Core.config.bundles_dir_name) + "\MOVIE2K.bundle\Contents\Services\URL\MOVIE2K\Modules\Patched\\runtime.py"
		docutilsPatchedFile = Core.storage.join_path(Core.app_support_path, Core.config.bundles_dir_name) + "\MOVIE2K.bundle\Contents\Services\URL\MOVIE2K\Modules\Patched\\docutils.py"
	else:
		if sys.platform.find('linux'):
			DictName = 'LD_LIBRARY_PATH'
		else:
			DictName = 'DYLD_LIBRARY_PATH'		
		runtime = Core.storage.join_path(Core.app_support_path, Core.config.bundles_dir_name) + "/Framework.bundle/Contents/Resources/Versions/2/Python/Framework/components/runtime.py"
		LocalFrameworkPath = Core.storage.join_path(Core.app_support_path, Core.config.bundles_dir_name) + "/Framework.bundle/Contents/Resources/Versions/2/Python/Framework/components"
		docutils = os.environ[DictName].split('Contents')[0] + "Contents/Resources/Plug-ins/Framework.bundle/Contents/Resources/Versions/2/Python/Framework/docutils.py"
		AppFramworkPath = os.environ[DictName].split('Contents')[0] + "Contents/Resources/Plug-ins/Framework.bundle/Contents/Resources/Versions/2/Python/Framework"
		runtimePatchedFile = Core.storage.join_path(Core.app_support_path, Core.config.bundles_dir_name) + "/MOVIE2K.bundle/Contents/Services/URL/MOVIE2K/Modules/Patched/runtime.py"
		docutilsPatchedFile = Core.storage.join_path(Core.app_support_path, Core.config.bundles_dir_name) + "/MOVIE2K.bundle/Contents/Services/URL/MOVIE2K/Modules/Patched/docutils.py"
		
	localHash = [Hash.SHA1(Core.storage.load(runtime)), Hash.SHA1(Core.storage.load(docutils))]
	patchedHash = [Hash.SHA1(Core.storage.load(runtimePatchedFile)), Hash.SHA1(Core.storage.load(docutilsPatchedFile))]
	PatchedFile = [runtimePatchedFile, docutilsPatchedFile]
	FrameworkPath = [LocalFrameworkPath, AppFramworkPath]
	ResetCore = False
	i = 0
	
	while i <= 1:
		if localHash[i] != patchedHash[i]:
			ResetCore = True
			Log("File runtime.py has changed - copying patched version.")
			Core.storage.copy(PatchedFile[i], FrameworkPath[i])
		i += 1
		
	if ResetCore == True:
		# Reload system services
		Core.services.load()
		Log("Reloaded system services")
		

####################################################################################################
@setInterval(10)
def CheckPrefsEnabled():
	global stopAutoResume
	global stopAutoPatcher
	
	# Check to see if autoResume Enabled/Disabled for Downloads that have failed
	if Prefs['autoresume'] == "Enabled":
		if stopAutoResume == None:
			Log("Autoresume Download Enabled!!!")
			stopAutoResume = AutoCheckMyDownload()
	elif Prefs['autoresume'] == "Disabled":
		if stopAutoResume != None:
			Log("Autoresume Download Disabled!!!")
			stopAutoResume.set()
			stopAutoResume = None
			
	# Check to see if autoPatcher Enabled/Disabled for runtime.py update
	if Prefs['autopatcher'] == "Enabled":
		if stopAutoPatcher == None:
			Log("Autopatcher Enabled!!!")
			stopAutoPatcher = CheckforRuntimeUpdate()
	elif Prefs['autopatcher'] == "Disabled":
		if stopAutoPatcher != None:
			Log("Autopatcher Disabled!!!")
			stopAutoPatcher.set()
			stopAutoPatcher = None

####################################################################################################
@setInterval(60)
def AutoCheckMyDownload():
	global MyDownloadPath
	global MyDownloadRequest
	global stopStitching
	global ResumeParts
	global ResumePath
	global isAwake
	global stop
	i = 1

	hosts = LoadData(fp=WATCHIT_DATA, GetJson=3)
	
	if isAwake == True:
		IamAwake = True
	else:
		isAwake = True
		IamAwake = False

	for gethost in hosts:
		if IamAwake == True:
			break
			
		path = gethost[i]['Path']
		host = gethost[i]['Host']
		videostreamlink = gethost[i]['VideoStreamLink']
		HostPage = gethost[i]['HostPage']
		url = gethost[i]['URL']
		LinkType = gethost[i]['LinkType']
		contentlength = gethost[i]['ContentLength']
		FileCheckSize = gethost[i]['FileCheckSize']
		resumepath = []
		resumepath.extend(gethost[i]['ResumePath'])
		resumecontentlength = gethost[i]['ResumeContentLength']
		resumecount = gethost[i]['ResumeCount']
		isStitchingFiles = gethost[i]['isStitchingFiles']

		if path != "":
			try:
				if isStitchingFiles == "True":
					part = os.stat(path).st_size
					percent = 100 * float(part)/float(contentlength)
					
					if percent == 100.00:
							gethost[i]['isStitchingFiles'] = "False"
							isStitchingFiles = "False"
				elif resumecontentlength == "":
					part = os.stat(path).st_size
					percent = 100 * float(part)/float(contentlength)

					LastTimeFileWrite = os.path.getmtime(path)
					LocalTime = time.time()
					ElapseTime = LocalTime - LastTimeFileWrite
				else:
					part = os.stat(path).st_size 
					for getPaths in resumepath:
						part = part + os.stat(getPaths).st_size
					percent = 100 * float(part)/float(contentlength)

					if percent == 100.0:
						gethost[i]['isStitchingFiles'] = "True"
						isStitchingFiles = "True"
						if stopStitching == None:
							stopStitching = StitchFilesTogether()
						ResumeParts = [path]+resumepath
						ResumePath = path.replace('Part1.', '')
						gethost[i]['Path'] = path.replace('Part1.', '')
						gethost[i]['ResumePath'] = []
						gethost[i]['ResumeContentLength'] = ""
					else:
						LastTimeFileWrite = os.path.getmtime(resumepath[-1])
						LocalTime = time.time()
						ElapseTime = LocalTime - LastTimeFileWrite
			except:
				Log("Error: %s file not found to play back." % path)
				part = 0
				FileCheckSize = 0
				percent = 0.0
				ElapseTime = 120.0
				isStitchingFiles = "False"
				gethost[i]['isStitchingFiles'] = "False"
				gethost[i]['ResumePath'] = []
				gethost[i]['ResumeContentLength'] = ""

			if percent == 100.0 or isStitchingFiles == "True":
				pass
			elif ElapseTime >= 120.0 and int(FileCheckSize) == part:
				if stop == None:
					stop = CheckForDownload()

				(NullPath, NewDownloadRequest, ResumeContentLength, GoodLink, VideoStreamLink) = ResumeMyDownload(Host=host, HostPage=HostPage, url=url, LinkType=LinkType, startByte=str(part), ContentLength=contentlength)

				Log("TRYING TO RESUME DOWNLOAD FROM AUTUTORESUEM: "+str(GoodLink))

				if int(ResumeContentLength) != int(contentlength) and GoodLink == True:
					if not "Part1." in path:
						os.renames(path, path.replace(DownloadPath, DownloadPath+'Part1.'))
						gethost[i]['Path'] = path.replace(DownloadPath, DownloadPath+'Part1.')
						NewDownloadPath = path.replace(DownloadPath, DownloadPath+'Part2.')
					else:
						partnum = len(resumepath) + 2
						NewDownloadPath = path.replace(DownloadPath+'Part1.', DownloadPath+'Part'+str(partnum)+'.')
	
					MyDownloadPath = NewDownloadPath
					gethost[i]['ResumePath'] = resumepath+[NewDownloadPath]
					gethost[i]['ResumeContentLength'] = str(ResumeContentLength)
				else:
					MyDownloadPath = path

				if GoodLink == True:
					MyDownloadRequest = NewDownloadRequest
					gethost[i]['FileCheckSize'] = "0"
					resumecount = int(resumecount) + 1
					gethost[i]['ResumeCount'] = str(resumecount)
					JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)
			else:
				gethost[i]['FileCheckSize'] = str(part)
				JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)

		i += 1
	if IamAwake == False:
		isAwake = False


####################################################################################################
def combine_files(parts, path):
	'''
	Function combines file parts.
	@param parts: List of file paths.
	@param path: Destination path.
	'''
	with open(path,'wb') as output:
		for part in parts:
			with open(part,'rb') as f:
				output.writelines(f.readlines())
			os.remove(part)


####################################################################################################
def downloads(VideoStreamLink, startByte="0", endByte=""):

	Log("DOWNLOAD URL: "+VideoStreamLink)
	try:
		video_url = VideoStreamLink.split("?cookies=")[0]
		cookies = ast.literal_eval(String.Unquote(VideoStreamLink.split("cookies=")[1].split("&")[0], usePlus=True))
		headers = ast.literal_eval(String.Unquote(VideoStreamLink.split("headers=")[1], usePlus=True))
		headers['Connection'] = 'keep-alive'
	except:
		video_url = VideoStreamLink
		headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'User-Agent': UserAgent, 'Connection': 'keep-alive'}
		cookies = {}

	if startByte != "0":
		headers['Range'] = 'bytes=%s-%s' % (startByte,endByte)

	session = requests.session()
	requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
	request = session.get(video_url, headers=headers, stream=True, allow_redirects=True)

	try:
		ContentLength = int(request.headers['Content-Length'].strip())
	except:
		ContentLength = -1

	Log("####################################################################################################")
	Log(request.headers)
	Log("####################################################################################################")
	Log("STATUS CODE: "+str(request.status_code))
	Log("####################################################################################################")
	Log("CONTENT-LENGTH: "+str(ContentLength))
	Log("####################################################################################################")

	if str(request.status_code) == "416":
		Log("Didn't get the file it was expecting. Retrying...")
		time.sleep(5)
		return downloads(VideoStreamLink, startByte, endByte)
	elif str(request.status_code) == "403":
		NoError = "Wrong IP was returned"
		request = None
	elif str(request.status_code) == "503":
		NoError = "the server is temporarily unavailable"
		request = None
	elif int(ContentLength) == 8 or int(ContentLength) == 15 or int(ContentLength) == 113244:
		NoError = "failed to start downloading"
		request = None
	else:
		NoError = True

	return (request, ContentLength, NoError)


####################################################################################################
def StartMyDownload(path, request):
	if not os.path.exists(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))

	with open(path, 'wb') as handle:
		for chunk in request.iter_content(chunk_size=1024):
       			if not chunk: # filter out keep-alive new chunks
				break
			handle.write(chunk)

	handle.close()


####################################################################################################
def MyDownload(VideoStreamLink, title=None, startByte="0", OldContentLength="0"):
	endByte = ""
	path = ""

	if startByte == "0":
		path = "Videos%s%s_%s.%s" % (DownloadPath, re.sub('\W', '_', str(title), flags=re.UNICODE), str(time.time()), VideoStreamLink.split('/')[-1].split('.')[1].partition('?')[0])


	(request, ContentLength, NoError) = downloads(VideoStreamLink, startByte, endByte)

	return (path, request, ContentLength, NoError)


####################################################################################################
def MyDownloadThread(path, request):
	thread = threading.Thread(target=StartMyDownload, args=(path, request,))
	#thread.setDaemon(True)
	threadList.append(thread)

	hosts = LoadData(fp=WATCHIT_DATA, GetJson=3)
	i = 1
	for gethost in hosts:
		if gethost[i]['Path'] == path:
			gethost[i]['Thread'] = str(thread)
			break
		else:
			i += 1
	JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)

	thread.start()

	#for myThreads in threadList:
	#	myThreads.join()

	#Log('Thread is not alive: ' + str(thread.is_alive()))


####################################################################################################
def KillMyDownloadThread(MyThread):
	global threadList

	for KillThread in threadList:
		if str(KillThread) == MyThread:
			if KillThread.isAlive():
				try:
					#KillThread.__stop = True
					KillThread._Thread__stop()
				except:
					Log(str(KillThread.getName()) + ' could not be terminated')


####################################################################################################
def ResumeMyDownload(Host, HostPage, url, LinkType, title=None, startByte="0", ContentLength="0"):
	request = None
	path = ""
 
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
		(path, request, ContentLength, NoError) = MyDownload(VideoStreamLink=VideoStreamLink, title=title, startByte=startByte, OldContentLength=ContentLength)

	return (path, request, ContentLength, NoError, VideoStreamLink)


####################################################################################################
def GetHostVideo(title, date, DateAdded, Quality, thumb, type, summary, directors, guest_stars, genres, duration, rating, season, index, content_rating, source_title, url, Host):

	(HostPage, LinkType) = GetHostPageURL(Host=Host, url=url)

	#Check For Real Host
	Host = HostPage.split('http://')[1].split('.')[0].capitalize()
	if Host == 'Www' or Host == 'Embed' or Host == 'Beta' or Host == 'Movie':
		Host = HostPage.split('http://')[1].split('.')[1].capitalize()

	(path, request, ContentLength, NoError, VideoStreamLink) = ResumeMyDownload(Host=Host, HostPage=HostPage, url=url, LinkType=LinkType, title=title)

	if NoError == True:
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
					hosts[jj][i]['HostPage'] = HostPage
					hosts[jj][i]['URL'] = url
					hosts[jj][i]['LinkType'] = LinkType
					hosts[jj][i]['ContentLength'] = ContentLength
					break
				else:
					i += 1
					jj += 1
			except:
				hosts.append({i : {'Type': type, 'Path': path, 'Host': Host, 'DateAdded': DateAdded, 'Quality': Quality, 'ThumbURL': thumb, 'Title': title, 'Summary':summary, 'Genres': genres, 'Directors': directors, 'GuestStars':guest_stars, 'Duration': duration, 'Rating': rating, 'Index': index, 'Season': season, 'ContentRating': content_rating, 'SourceTitle': source_title, 'Date': date, 'VideoType': videotype, 'VideoStreamLink': VideoStreamLink, 'HostPage': HostPage, 'URL': url, 'LinkType': LinkType, 'ContentLength': ContentLength, 'FileCheckSize': '0', 'ResumePath': [], 'ResumeContentLength': '', 'ResumeCount': '0', 'Thread': '', 'FailedFileDeletion': '', 'isStitchingFiles': 'False'}})
				break

		JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)

	return (path, request, NoError)

		
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
			if type(gethost[i]['ResumePath']) != type(list()):
				ResumePath = gethost[i]['ResumePath']
				gethost[i]['ResumePath'] = [ResumePath]
		except:
			gethost[i].update({'ResumePath': []})
		try:
			gethost[i]['ResumeContentLength']
		except:
			gethost[i].update({'ResumeContentLength': ''})
		try:
			gethost[i]['ResumeCount']
		except:
			gethost[i].update({'ResumeCount': '0'})
		try:
			gethost[i]['Thread']
		except:
			gethost[i].update({'Thread': ''})
		try:			
			gethost[i]['isStitchingFiles']
		except:
			gethost[i].update({'isStitchingFiles': 'False'})
			
		i += 1

	JsonWrite(fp=WATCHIT_DATA, jsondata=hosts)