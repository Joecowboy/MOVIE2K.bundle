####################################################################################################
# Setting up imports

import inspect, os, sys
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
import urllib2
import re
import time
import random
import base64

from ordereddict import OrderedDict
from HostServices import ScriptConvert
from HostServices import ScriptDecode
from HostServices import zDecrypt
from HostServices import decodeurl
from HostServices import CharConvert
from HostServices import SecondButtonPress
from HostServices import SoftCaptcha
from HostServices import SolveMediaCaptcha
from HostServices import GoogleCaptcha
from HostServices import ErrorMessage
from HostServices import IncapsulaScript
from HostServices import CookieDict


####################################################################################################
def GetMovie(Host, HostPage, url, LinkType):

	#################################
	#Trailer Addict
	#################################
	if Host == 'TrailerAddict':
		headers = {'User-Agent': UserAgent, 'Referer': HostPage}
		session = requests.session()
		req = session.get(HostPage, headers=headers)
		cookies = CookieDict(cookies=session.cookies)
		trailerurlID = req.content.split('name="movie" value="')[1].split('"')[0].split('/')[4]
		trailerurlCFG = 'http://www.traileraddict.com/fvar.php?tid=' + trailerurlID
		trailer_url = requests.get(trailerurlCFG, headers=headers).content.split('fileurl=')[1].split('&')[0]
		VideoStream = trailer_url + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)

	#################################
	#Select Movide2k Video Hoster
	#################################
	elif Host == "180upload" or Host == "180upload_2":
		try:
			if Host == "180upload":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host)
			elif Host == "180upload_2":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=2)

			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoStream = ScriptConvert(script=VideoInfo)
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="main"]/div/b')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
				except:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="err"]')[0].text_content().strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")

			if Host == "180upload":
				VOID = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=1)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "2gb-hosting":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="container"]/div/div/video/source')[0].get('src')
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="alert alert-danger"]')[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Allmyvideos":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				try:
					VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[2].text.split('"file" : "')[2].split('"')[0]
				except:
					VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[2].text.split('"file" : "')[1].split('"')[0]
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="content"]/div')[0].text_content.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Altervideo":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'WATCH': 'true'})
			try:
				VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="minimalist flowplayer is-mouseout"]/video/source')[0].get('src')
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="alert alert-danger alert-dismissable"]')[0].text_content().strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Anonstream":
			VideoStream = ErrorMessage(Host=Host, LogError=3, ErrorType="HostDown")
	elif Host == "Barbavid":
		try:
			headers = {'User-Agent': UserAgent, 'Host': 'barbavid.com'}
			payload = {}
			session = requests.session()
			s = session.get(HostPage, headers=headers)
			cookies = CookieDict(cookies=session.cookies)
			VideoInfo = HTML.ElementFromString(s.content).xpath('//div[@id="player"]/object/param')[1].get('value')
			payload[VideoInfo.split('=')[0]] = VideoInfo.split('=')[1].split('&')[0]
			video_url1 = "http://barbavid.com/datazz2.php"
			VideoID = session.post(video_url1, data=payload, headers=headers, cookies=cookies)
			payload = {"chunk": urllib.quote_plus(VideoID.content.split('chunk_1=')[1].split('&')[0]), "video": VideoID.content.split('file_md5=')[1].split('&')[0], "yarbamonkst": "yunburangeoo"}
			video_url2 = "http://barbavid.com/smonker.php"
			VideoKEY = session.post(video_url2, data=payload, headers=headers, cookies=cookies)
			VideoURL = "http://"+VideoID.content.split('server=')[1].split('&')[0]+".barbavid.com/play?video="+VideoID.content.split('file_md5=')[1].split('&')[0]+"&chunk="+VideoID.content.split('chunk_1=')[1].split('&')[0]+"&key="+VideoKEY.content.split('var1=')[1].split('&')[0]
			headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': 'http://barbavid.com/player.swf'}
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=5)
	elif Host == "Bestreams":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'referer': url})
			VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
			VideoStream = VideoInfo.split('file: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=3, ErrorType="HostDown")
	elif Host == "Billionuploads":
		try:
			if LinkType == 1:
				HostPage = "http://billionuploads.com/"+HostPage.split('-')[1]

			headers = OrderedDict()
			headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
			headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
			headers['Accept-Encoding'] = 'gzip,deflate,sdch'
			headers['Accept-Language'] = 'en-US,en;q=0.8'
			headers['Cache-Control'] = 'max-age=0'
			headers['Connection'] = 'keep-alive'
			headers['Referer'] = url
			headers['User-Agent'] = UserAgent
			session = requests.session()
			s = session.get(HostPage, headers=headers)
			try:
				IncapsulaPage = "http://billionuploads.com" + HTML.ElementFromString(s.content).xpath('//head/iframe')[0].get('src')
				s = session.get(IncapsulaPage, headers=headers)
			except:
				VideoInfo = HTML.ElementFromString(s.content).xpath('//head/script')[1].text
				IncapsulaPage = IncapsulaScript(DeString=VideoInfo)
				s1 = session.get(IncapsulaPage, headers=headers)

			cookies = CookieDict(cookies=session.cookies)
			session1 = requests.session()
			requests.utils.add_dict_to_cookiejar(session1.cookies, cookies)
			VideoPage = session1.get(HostPage, headers=headers)
			cookies = CookieDict(cookies=session1.cookies)
			KeyValue = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="dobox"]/textarea')[0].text
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, page=VideoPage, addkey={"submit_btn": "", "down_direct": "1", "blader": KeyValue, "airman": "toast"}, removekey=["rand", "sys"], cookies=cookies)

			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div [@id=\'inf\']/input[@id="dl"]')[0].get('value').split('GvaZu')[1]
				VideoStream = VideoInfo.decode('base64', 'strict').decode('base64', 'strict')
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="container"]/div[@class="centered"]/div/div')[0].text_content.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Bitloader":
		try:
			VideoID = HostPage.split('/')[4]
			VideoPageXML = "http://bitloader.org/Xajax/saveaction/?xjxfun=load_player_eng&xjxr="+str(time.time())+"&xjxargs[]=S"+VideoID+"&xjxargs[]=N5&xjxargs[]=Sip"
			VideoInfo = XML.ElementFromURL(VideoPageXML)
			try:
				VideoStream = VideoInfo.xpath('//cmd')[0].text.split('&file=')[1].split('"')[0]
			except:
				VideoError = VideoInfo.xpath('//xjx')[0].text
				if VideoError == None:
					InputError = "Video has been removed!"
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Bitshare":
		try:
			VideoPage = HTML.ElementFromURL(HostPage)
			try:
				VideoInfo = VideoPage.xpath('//div[@id="stream_flash"]/script')[1].text
				VideoStream = VideoInfo.split('clip: {')[1].split("url: '")[1].split("'")[0]
			except:
				InputError = VideoPage.xpath('//div[@id="content"]/h1')[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Boojour":
		try:
			headers = {'User-Agent': UserAgent, 'Host': 'www.boojour.eu'}
			session = requests.session()
			VideoPage = session.get(HostPage, headers=headers)
			try:
				cookies = (CookieDict(cookies=session.cookies))
				removekey=[]
				VideoInfo = HTML.ElementFromString(VideoPage.content)
				removekey1 = VideoInfo.xpath('//form[@method="post"]/input')[1].get('name')
				removekey.append(removekey1)
				try:
					checkkey2 = VideoInfo.xpath('//form[@method="post"]/input')[2].get('disabled')
					if checkkey2 == "disabled":
						removekey2 = VideoInfo.xpath('//form[@method="post"]/input')[2].get('name')
						removekey.append(removekey2)
				except:
					pass
				try:
					checkkey3 = VideoInfo.xpath('//form[@method="post"]/input')[3].get('disabled')
					if checkkey3 == "disabled":
						removekey3 = VideoInfo.xpath('//form[@method="post"]/input')[3].get('name')
						removekey.append(removekey3)
				except:
					pass
				VideoPage = SecondButtonPress(url=url, HostPage=HostPage, page=VideoPage, addkey={"x": random.randrange(0, 178, 2), "y": random.randrange(0, 68, 2)}, removekey=removekey, cookies=cookies)
				VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="container"]/div/a')[0].get('href')
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//h1')[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Clicktoview" or Host == "Clicktoview_2":
		try:
			if Host == "Clicktoview":
				VideoInfo = SecondButtonPress(url=url, HostPage=HostPage, addkey={"referer": url})
				VideoPage = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, VideoInfo=VideoInfo.content, cookies=VideoInfo.cookies)
			elif Host == "Clicktoview_2":
				VideoPage = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=2)

			try:
				VideoScript = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
				VideoStream = ScriptConvert(script=VideoScript)
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="err"]')[0].text_content().strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")
				except:			
					InputError = HTML.ElementFromString(VideoInfo.content).xpath('//font[@color="red"]')[1].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")

			if Host == "Clicktoview":
				VideoInfo = SecondButtonPress(url=url, HostPage=HostPage, addkey={"referer": url})
				VOID = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, VideoInfo=VideoInfo.content, RecaptchaResponse=1, cookies=VideoInfo.cookies)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Cloudvidz":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				VideoInfo = SecondButtonPress(url=url, HostPage=HostPage, page=VideoPage, addkey={"down_script": "1"})
				VideoScript = HTML.ElementFromString(VideoInfo.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoStream = ScriptConvert(script=VideoScript)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="col-lg-10 col-lg-offset-1"]/b')[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Cubtv":
		try:
			VideoStream = HTML.ElementFromURL(HostPage).xpath('//head/script')[3].text.split("'file':'")[1].split("'")[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Cyberlocker":
		VideoStream = ErrorMessage(Host=Host, LogError=3, ErrorType="HostDown")
	elif Host == "Daclips":
		try:
			headers = {'User-Agent': UserAgent[UserAgentNum], 'Host': 'daclips.in'}
			session = requests.session()
			VideoPage = session.get(HostPage, headers=headers)
			VideoInfo = HTML.ElementFromString(VideoPage.content)
			try:
				VideoStream = VideoInfo.xpath('//div[@id="player_code"]/script')[2].text.split('file: "')[1].split('"')[0]
			except:
				InputError = VideoInfo.xpath('//span[@id="head_title"]')[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Datacloud":
		try:
			session = requests.session()
			url = HostPage+"/r"
			headers = {'Host': 'datacloud.to', 'Referer': HostPage+'/c', 'User-Agent': UserAgent}
			cookies = {}
			s = session.get(HostPage, headers=headers)
			cookies = CookieDict(cookies=session.cookies)
			captchaimg = "http://datacloud.to" + HTML.ElementFromString(s.content).xpath('//img[@class="captcha_img"]')[0].get('src')
			captchakey = GetImgValue(url=captchaimg, UserAgent=UserAgent, cookies=cookies, split=None).replace('-', '')
			payload = {'action': 'checkCapchaDownload', 'captcha': captchakey, 'link': HostPage.split('/')[4]}
			FormURL = "http://datacloud.to/process"
			req = session.post(FormURL, data=payload, headers=headers)
			OpenUrl = session.get(url, headers=headers)
			VideoStream = "http://" + OpenUrl.content.split('<div class="download_buttons">')[1].split('<script type="text/javascript">')[1].split('files = "')[1].split('?')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=3, ErrorType="HostDown")
	elif Host == "Divxhosted":
		try:
			VideoID = HostPage.split('/')[4]
			VideoPageXML = "http://divxhosted.com/Xajax/saveaction/?xjxfun=load_player_eng&xjxr="+str(time.time())+"&xjxargs[]="+VideoID+"&xjxargs[]=N2"
			VideoInfo = XML.ElementFromURL(VideoPageXML)
			try:
				VideoStream = VideoInfo.xpath('//cmd')[0].text.split('&file=')[1].split('"')[0]
			except:
				InputError = VideoInfo.xpath('//xjx')[0].text
				if InputError == None:
					InputError = "404 Page not found"
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Divxhosting":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"goto": "divx"})
			try:
				VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="video"]/object/param')[3].get('value')
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="alert alert-error span8"]')[0].text_content().strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Divxmotion":
		try:
			#Iframe Links to other sites....
			VideoPage = HTML.ElementFromURL(HostPage).xpath("//div[@class='post-body']/p/iframe")[0].get('src')
			Host = VideoPage.split('/')[2].split('.')[0].capitalize()
			if Host == 'Www' or Host == 'Embed':
				Host = VideoPage.split('/')[2].split('.')[1].capitalize()
			VideoStream = GetMovie(Host=Host, HostPage=VideoPage, url=url, LinkType=1)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Divxstage":
		try:
			if LinkType == 4:
				VideoInfo = HTML.ElementFromURL(HostPage).xpath('//div[@id="video_page"]/script[@type="text/javascript"]')[2].text
			elif LinkType == 1:
				VideoInfo = HTML.ElementFromURL(HostPage).xpath('//script[@type="text/javascript"]')[5].text
			try:
				CodeString = VideoInfo.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[2].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				VideoID = CharSrc.split('flashvars.file=')[1].split('"')[1]
				VideoKey = urllib.quote(CharSrc.split('flashvars.filekey=')[1].split('"')[1])
			except:
				VideoID = VideoInfo.split('flashvars.file="')[1].split('"')[0]
				VideoKey = VideoInfo.split('fkz="')[1].split('"')[0]
			url = "http://www.divxstage.eu/api/player.api.php?numOfErrors=0&file="+VideoID+"&user=undefined&key="+VideoKey+"&cid=undefined&pass=undefined&cid2=undefined&cid3=undefined"
			headers = {'User-Agent': UserAgent, 'Host': 'www.divxstage.eu', 'Referer': 'http://embed.divxstage.eu/player/divxstage-v5.swf'}
			session = requests.session()
			VideoInfo =  session.get(url, headers=headers)
			VideoStream = VideoInfo.content.split('=')[1].split('&')[0]
			if VideoStream == "1":
				InputError = VideoInfo.content.split('=')[2]
				if InputError == "Incorrect IP. Please refresh!!":
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongIP")
				else:
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Donevideo":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, elm='div[@id="adsdiv2"]/', addkey={"referer": url})
			try:
				VideoInfo = SecondButtonPress(url=HostPage, HostPage=HostPage, page=VideoPage, elm='div[@class="content_area"]//', addkey={"referer": url})
				VideoID = HTML.ElementFromString(VideoInfo.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoURL = ScriptConvert(script=VideoID)
				cookies = {'ref_url': urllib.quote_plus(HostPage)}
				headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': 'http://videozed.net/player/player.swf'}
				VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="content_area"]/h2')[0].text + " - File Not Found"
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Dotsemper":
		VideoStream = ErrorMessage(Host=Host, LogError=3, ErrorType="HostDown")
	elif Host == "Dwn":
		try:
			VideoPage = HTML.ElementFromURL(HostPage).xpath('//div[@id="query"]/div/iframe')[0].get('src')
			VideoID = HTML.ElementFromURL(VideoPage).xpath('//body/script')[0].text.split("SWFObject('")[1].split("'")[0]
			VideoInfo = "http://st.dwn.so/xml/videolink.php?"+VideoID.split('?')[1]+"&width=830&id="+str(time.time())+"&u=undefined"
			headers = {'User-Agent': UserAgent, 'Referer': VideoID}
			VideoXML = requests.get(VideoInfo, headers=headers)
			try:
				VideoStream = "http://" + VideoXML.content.split('un="')[1].split('"')[0]
			except:
				InputError = VideoXML.content.split('errortext="')[1].split('"')[0]
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Ecostream":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage+"?ss=1")
			VideoInfo = VideoPage.content.split('<script type="text/javascript">')[1].split("','")
			url = "http://www.ecostream.tv/lo/mq.php"
			files = {}
			payload = {"s" : HostPage.split('/')[4].split('.')[0], "k": VideoInfo[1], "t": VideoInfo[2], "key": VideoInfo[3].split("'")[0]}
			headers = {'User-Agent': UserAgent, 'Referer': HostPage, 'Host': 'www.ecostream.tv', 'X-Requested-With':'XMLHttpRequest'}
			session = requests.session()
			VideoID = session.post(url, data=payload, headers=headers, files=files)
			VideoStream = "http://www.ecostream.tv"+String.Unquote(VideoID.content.split('flashvars="file=')[1].split('&')[0])
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Entroupload":
		try:
			cookies = {'lang': 'english', 'ref_url': urllib.quote_plus(url)}
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, cookies=cookies, addkey={"referer": url})
			VideoID = VideoPage.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split('</script>')[0]
			VideoURL = ScriptConvert(script=VideoID)
			headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': HostPage}
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Faststream" or Host == "Fastsream":
		try:
			if LinkType == 4:
				HostPage = "http://faststream.in/embed-" + HostPage.split('/')[3] + "-720x480.html"
			VideoPage = HTML.ElementFromURL(HostPage)
			try:
				VideoStream = VideoPage.xpath('//div[@id="player_code"]/script')[1].text.split('file: "')[1].split('"')[0] + "?start=0"
			except:
				InputError = VideoPage.text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Filebox":
		VideoStream = ErrorMessage(Host=Host, LogError=3, ErrorType="HostDown")
	elif Host == "Filego":
		try:
			VideoPage = 'http://www.filego.org/fgflash.php?id=' + HostPage.split('=')[1]
			VideoInfo = HTML.ElementFromURL(VideoPage).xpath('//body/script[@type="text/javascript"]')[0].text
			VideoID = VideoInfo.split('function square()')[1].split('}')[0]
			VideoURL = VideoID.split("='")
			VideoStream = VideoURL[7].split("'")[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Fileloby" or Host == "Fileloby_2":
		try:
			if Host == "Fileloby":
				url = HostPage
				HostPage = HostPage + "?d=1"
				headers = {'User-Agent': UserAgent, 'Referer': url}
				session = requests.session()
				OpenUrl = session.get(url, headers=headers)
				time.sleep(10)
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, elm='div[@class="captchaPageTable"]/', elm2='table/tbody/tr/td/div/div/', Host=Host, SessionCookies=session.cookies)
			elif Host == "Fileloby_2":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, elm='div[@class="captchaPageTable"]/', elm2='table/tbody/tr/td/div/div/', Host=Host, RecaptchaResponse=2)

			try:
				VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="bodyBar"]/script')[1].text.split('m4v: "')[1].split('"')[0]
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="form-join"]/table//div/div')[2].text_content().strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
				except:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//form[@id="form-join"]/table//div/div')[2].text_content().strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")

			if Host == "Fileloby":
				OpenUrl = session.get(url, headers=headers)
				time.sleep(10)
				VOID = SolveMediaCaptcha(url=url, HostPage=HostPage, elm='div[@class="captchaPageTable"]/', elm2='table/tbody/tr/td/div/div/', Host=Host, RecaptchaResponse=1, SessionCookies=session.cookies)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Filenuke":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, elm='div[@id="content"]//', addkey={'method_free': 'Free'}, cookies={'cf_use_ob': '0'})
			try:
				try:
					VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
				except:
					VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoURL = ScriptConvert(script=VideoInfo)
				cookies = {'cf_use_ob': '0', 'lang': 'english', 'ref_ur': urllib.quote_plus(url)}
				headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': 'http://filenuke.com/player/player.swf'}
				VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//center[@id="cent"]/div')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Filezy":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"method_free_rt": "Free Download", "referer": url})
			VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/object/embed')[0].get('src')
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Flashstream":
		try:
			VideoPage = HTML.ElementFromURL(HostPage)
			try:
				VideoInfo = VideoPage.xpath('//div[@id="player_code"]/script')[1].text
			except:
				VideoInfo = VideoPage.xpath('//div[@id="player_code"]/script')[0].text
			VideoURL = ScriptConvert(script=VideoInfo)
			cookies = {'lang': 'english', 'domain': '.flashstream.in', 'path': '/'}
			headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': 'http://flashstream.in/player/player.swf'}
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Flashvids":
		try:
			VideoID = HostPage.split('/')[4]
			VideoPageXML = "http://flashvids.org/Xajax/saveaction/?xjxfun=load_player_eng&xjxr="+str(time.time())+"&xjxargs[]="+VideoID+"&xjxargs[]=N3"
			VideoStream = XML.ElementFromURL(VideoPageXML).xpath('//cmd')[0].text.split('&file=')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Flashx":
		try:
			Removed = False
			cookies = {}
			session = requests.session()
			headers = {'User-Agent': UserAgent, 'Host': 'flashx.tv', 'Referer': url}

			if LinkType == 4:
				s = session.get(HostPage, headers=headers)
				try:
					VideoInfo = HTML.ElementFromString(s.content).xpath('//div[@id="normal_player_cont"]/iframe')[0].get('src')
					cookies = CookieDict(cookies=session.cookies)
				except:
					Removed = True
					InputError = HTML.ElementFromString(s.content).xpath('//div[@class="cb_error"]//center')[0].text_content().strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
			elif LinkType == 1:
				VideoInfo = HostPage

			if Removed == False:
				v = SecondButtonPress(url=url, HostPage=VideoInfo, cookies=cookies)
				try:
					VideoLink = HTML.ElementFromString(v.content).xpath('//head/script')[0].text.split('config=')[1].split('"')[0]
					headers['Host'] = 'play.flashx.tv'
					headers['Referer'] = HTML.ElementFromString(v.content).xpath('//head/script')[0].text.split('data="')[1].split('"')[0]
					xmlreq = session.get(VideoLink, headers=headers)
					if xmlreq.content.split('<config>')[1].strip() == "wrong user/ip 1":
						InputError = xmlreq.content.split('<config>')[1].strip()
						VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongIP")
					else:
						VideoStream = XML.ElementFromString(xmlreq.content).xpath('//file')[0].text + "?start=0"
				except:
					InputError = HTML.ElementFromString(v.content).xpath('//font[@class="red"]')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Fleon":
		try:
			VideoPage = "http://fleon.me/videos.php?Id="+HostPage.split('=')[1]
			VideoInfo = HTML.ElementFromURL(VideoPage).xpath('//div[@class="containerDiv"]/script')[1].text
			vidstr = 'mp4:' + VideoInfo.split("file','")[1].split("'")[0]
			swfurl = VideoInfo.split("SWFObject('")[1].split("'")[0]
			url_MO = int(swfurl.split('/')[3].split('.')[0])
			rtmpurl = ["", "rtmp://213.163.74.241/vod", "rtmp://213.163.74.225/vod", "rtmp://213.163.74.229/vod", "rtmp://213.163.74.233/vod", "rtmp://213.163.74.237/vod"]
			VideoStream = [vidstr, swfurl, rtmpurl[url_MO], 'rtmp', VideoPage, 'vod']
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Gigabyteupload":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'submit': 'watch'})
			VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="video-player"]/div/video/source')[0].get('src')
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Ginbig":
		#Host is not around any more
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			VideoInfo = VideoPage.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split('</script>')[0]
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=3, ErrorType="HostDown")
	elif Host == "Gorilla-tube":
		try:
			VideoID = HostPage.split('/')[4]
			VideoPageXML = "http://gorilla-tube.net/Xajax/saveaction/?xjxfun=load_player_eng&xjxr="+str(time.time())+"&xjxargs[]="+VideoID+"&xjxargs[]=N6"
			VideoStream = XML.ElementFromURL(VideoPageXML).xpath('//cmd')[0].text.split('&file=')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Gorillavid":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, elm='div[@id="content"]/', addkey={'referer': url})
			VideoStream = VideoPage.content.split('<div id="player_code"')[1].split('file: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Grifthost" or Host == "Grifthost_2":
		try:
			if Host == "Grifthost":
				VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'referer': url})
				VideoPage = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, VideoInfo=VideoPage.content, cookies=VideoPage.cookies)

			elif Host == "Grifthost_2":
				VideoPage = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=2)

			try:
				VideoScript = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/div[@id="player_code"]/script')[1].text
				VideoStream = ScriptConvert(script=VideoScript)
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="err"]')[0].text
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")
				except:			
					InputError = HTML.ElementFromString(VideoInfo.content).xpath('//div[@class="content_middle_big"]/h3')[0].text
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")

			if Host == "Grifthost":
				VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'referer': url})
				VOID = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, VideoInfo=VideoPage.content, RecaptchaResponse=1, cookies=VideoPage.cookies)

		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Hdvid":
		try:
			VideoPage = "http://hdvid.ws/videos.php?Id="+HostPage.split('=')[1]
			VideoInfo = HTML.ElementFromURL(VideoPage).xpath('//div[@class="containerDiv"]/script')[1].text
			vidstr = 'mp4:' + VideoInfo.split("file','")[1].split("'")[0]
			swfurl = VideoInfo.split("SWFObject('")[1].split("'")[0]
			url_MO = int(swfurl.split('/')[3].split('.')[0])
			rtmpurl = ["", "rtmp://213.163.74.241/vod", "rtmp://213.163.74.225/vod", "rtmp://213.163.74.229/vod", "rtmp://213.163.74.233/vod", "rtmp://213.163.74.237/vod"]
			VideoStream = [vidstr, swfurl, rtmpurl[url_MO], 'rtmp', VideoPage, 'vod']
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Hostingcup":
		try:
			headers = {'User-Agent': UserAgent}
			VideoPage = requests.get(HostPage, headers=headers)
			VideoID = HTML.ElementFromString(VideoPage.content).xpath('//object[@id="flvplayer"]/param')[4].get('value').split('levels=')[1].split('&')[0]
			VideoStream = String.Unquote(VideoID).split('file":"')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Hostingbulk":
		try:
			VideoStream = HTML.ElementFromURL(HostPage).xpath('//div[@class="portlet-content"]/center/div/table/tr/td/div/script')[1].text.split("'file': '")[1].split("'")[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Hqvideo":
		try:
			VideoPage = "http://hqvideo.cc/playerframe.php?Id="+HostPage.split('/')[4]
			VideoInfo = HTML.ElementFromURL(VideoPage).xpath('//div[@class="containerDiv"]/script')[1].text
			vidstr = 'mp4:' + VideoInfo.split("file','")[1].split("'")[0]
			swfurl = VideoInfo.split("SWFObject('")[1].split("'")[0]
			url_MO = int(swfurl.split('/')[3].split('.')[0])
			rtmpurl = ["", "rtmp://213.163.74.241/vod", "rtmp://213.163.74.225/vod", "rtmp://213.163.74.229/vod", "rtmp://213.163.74.233/vod", "rtmp://213.163.74.237/vod"]
			VideoStream = [vidstr, swfurl, rtmpurl[url_MO], 'rtmp', VideoPage, 'vod']
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Hugefiles":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, elm='div[@class="content-bg-repeat"]//div[@id="plans_free"]/center/', addkey={"referer": url})
			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoURL = ScriptConvert(script=VideoInfo)
				cookies = {'ref_url': urllib.quote_plus(url), 'domain': '.hugefiles.net'}
				headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': HostPage}
				VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="header"]/b')[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Ishared":
		try:
			VideoPage = HTML.ElementFromURL(HostPage)
			if LinkType == 4:
				VideoInfo = VideoPage.xpath('//body/script')[2].text
			elif LinkType == 1:
				VideoInfo = VideoPage.xpath('//body/script')[0].text
			VideoStream = VideoInfo.split('path:"')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Lemuploads"or Host == "Lemuploads_2":
		try:
			if Host == "Lemuploads":
				session = requests.session()
				headers = {'Host': 'lemuploads.com', 'Referer': url, 'User-Agent': UserAgent}
				VideoInfo = session.get(HostPage, headers=headers)
				VideoPage = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, VideoInfo=VideoInfo.content, cookies=session.cookies)
			elif Host == "Lemuploads_2":
				VideoPage = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=2)

			try:
				VideoScript = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoStream = ScriptConvert(script=VideoScript)
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="err"]')[0].text
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")
				except:			
					InputError = HTML.ElementFromString(VideoInfo.content).xpath('//div[@class="wrapper"]/div[@class="wrapper"]/div/b')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")

			if Host == "Lemuploads":
				session = requests.session()
				VideoInfo = session.get(HostPage, headers=headers)
				VOID = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, VideoInfo=VideoInfo.content, RecaptchaResponse=1, cookies=session.cookies)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Limevideo":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"referer": url})
			VideoInfo = SecondButtonPress(url=HostPage, HostPage=HostPage, page=VideoPage, addkey={"down_direct": 1, "referer": url, "method_premium": ""})
			VideoID = VideoInfo.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split('</script>')[0]
			VideoURL = ScriptConvert(script=VideoID)
			cookies = {'ref_url': urllib.quote_plus(HostPage)}
			headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': 'http://videozed.net/player/player.swf'}
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Megafiles":
		try:
			if LinkType == 4:
				HostPage = "http://www.megafiles.se/embed-"+HostPage.split('/')[3]+"-640x360.html"

			VideoInfo = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script')[1].text
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Megarelease"or Host == "Megarelease_2":
		try:
			if Host == "Megarelease":
				session = requests.session()
				headers = {'Host': 'megarelease.org', 'Referer': url, 'User-Agent': UserAgent}
				VideoInfo = session.get(HostPage, headers=headers)
				VideoPage = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, VideoInfo=VideoInfo.content, cookies=session.cookies)
			elif Host == "Megarelease_2":
				VideoPage = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=2)

			try:
				VideoScript = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoStream = ScriptConvert(script=VideoScript)
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="err"]')[0].text_content().strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")
				except:			
					InputError = HTML.ElementFromString(VideoInfo.content).xpath('//div[@class="wrapper"]/div[@class="wrapper"]/b')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")

			if Host == "Megarelease":
				session = requests.session()
				VideoInfo = session.get(HostPage, headers=headers)
				VOID = GoogleCaptcha(url=url, HostPage=HostPage, Host=Host, VideoInfo=VideoInfo.content, RecaptchaResponse=1, cookies=session.cookies)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Megavideoz":
		try:
			url = 'http://megavideoz.eu/get_video.php'
			params = {"v": HostPage.split('/')[4], "start": "0"}
			session = requests.session()
			headers = {'User-Agent': UserAgent, 'Host': 'megavideoz.eu', 'Referer': 'http://megavideoz.eu/player/cbplayer/player.swf'}
			cookies = {"pageredir": urllib.quote_plus(HostPage)}
			s = session.get(url, headers=headers)
			cookies = CookieDict(cookies=session.cookies)
			VideoID = session.head(url, params=params, headers=headers, cookies=cookies)
			VideoStream = VideoID.headers['Location'] + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Mightyload":
		try:
			VideoPage = HTML.ElementFromURL(HostPage).xpath('//div[@id="content"]/script')[2].text
			VideoStream = VideoPage.split("url: '")[4].split("'")[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Mightyupload":
		try:
			headers = {'User-Agent': UserAgent, 'Host': 'mightyupload.com', 'Referer': 'http://mightyupload.com/player510/player.swf'}
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"method_premium": "", "down_direct": "1", "referer": url})
			cookies = CookieDict(cookies=VideoPage.cookies)
			try:
				try:
					VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
					VideoStream = VideoInfo.split("file: '")[1].split("'")[0] + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
				except:
					VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
					VideoStream = ScriptConvert(script=VideoInfo) + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="extra"]/div[@class="main"]/b')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Miivideos":
		try:
			headers = {'User-Agent': UserAgent, 'Host': 'www.miivideos.com', 'Referer': HostPage}
			VideoInfo = "http://www.miivideos.com/videos.php?vid="+HostPage.split('_')[1].split('.')[0]
			session = requests.session()
			VideoPage = session.head(VideoInfo, headers=headers)
			VideoStream = VideoPage.headers['Location']
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Miloyski":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"submit": "watch"})
			VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="container content"]/div/div/video/source')[0].get('src')
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Mk-tube":
		try:
			VideoPage = HTML.ElementFromURL(HostPage).xpath('//div[@class="zn_post_wrap"]/a')[0].get('href')
			VideoStream = HTML.ElementFromURL(VideoPage).xpath('//a[@id="player"]')[0].get('href')
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Mojoload":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"method_free": "Free Download", "referer": url})
			VideoInfo = VideoPage.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split('</script>')[0]
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Mooshare":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, elm='section[@id="wrap"]/center/', addkey={"imhuman": "Proceed to video"}, wait=6)
			VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/div[@id="flvplayer_wrapper"]//script')[1].text
			swfurl = "http://muchshare.net/player/player.swf"
			vidstr = VideoInfo.split('file: "')[1].split('"')[0]
			rtmpurl = VideoInfo.split('streamer: "')[1].split('"')[0]
			app = VideoInfo.split('streamer: "')[1].split('"')[0].split('/')[3]
			VideoStream = [vidstr, swfurl, rtmpurl, 'rtmp', HostPage, app]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Movdivx":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
			except:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Movpod":
		try:
			cookies = {'ad_referer': url+str(time.time()), 'path': '/', 'domain': '.movpod.in'}
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, cookies=cookies, wform=1, wait=5, addkey={'referer': url})
			VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[2].text
			VideoStream = VideoInfo.split('file: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=2)
	elif Host == "Movreel":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'down_script': '1'})
			VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Movshare":
		try:
			VideoInfo = HTML.ElementFromURL(HostPage).xpath('//div[@id="mainContent"]/table//script[@type="text/javascript"]')[5].text
			try:
				CodeString = VideoInfo.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[2].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				VideoKey = urllib.quote(ScriptConvert(script=CharSrc))
				VideoID = HostPage.split('/')[4]
			except:
				VideoID = VideoInfo.split('flashvars.file="')[1].split('"')[0]
				VideoKey = VideoInfo.split('flashvars.filekey="')[1].split('"')[0]
			url = "http://www.movshare.net/api/player.api.php?cid2=undefined&cid=1&key="+VideoKey+"&cid3=movie2k%2Etl&numOfErrors=0&file="+VideoID+"&user=undefined&pass=undefined"
			headers = {'User-Agent': UserAgent, 'Host': 'www.movshare.net', 'Referer': 'http://www.movshare.net/player/movshare-v5.swf'}
			session = requests.session()
			VideoInfo =  session.get(url, headers=headers)
			VideoStream = VideoInfo.content.split('=')[1].split('&')[0]
			if VideoStream == "1":
				InputError = VideoInfo.content.split('=')[2]
				if InputError == "Incorrect IP. Please refresh!!":
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongIP")
				else:
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Muchshare":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"method_free": "Proceed to video"})
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, page=VideoPage)
			VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/div[@id="flvplayer_wrapper"]/script')[1].text
			swfurl = "http://muchshare.net/player/player.swf"
			vidstr = VideoInfo.split('file: "')[1].split('"')[0]
			rtmpurl = VideoInfo.split('streamer: "')[1].split('"')[0].split('?')[0]
			app = "vod"
			VideoStream = [vidstr, swfurl, rtmpurl, 'rtmp', HostPage, app]
			
			#VideoInfo = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script')[1].text
			#VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Nosvideo":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'down_script': '1', 'method_free': 'Continue to Video'})
			try:
				VideoID = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[2].text.split("php|")[1].split('|')[0]
				VideoPageXML = "http://nosvideo.com/xml/"+VideoID+".xml"
				headers = {'User-Agent': UserAgent, 'Host': 'nosvideo.com', 'Referer': HostPage}
				VideoInfo =  requests.get(VideoPageXML, headers=headers)
				VideoStream = VideoInfo.content.split('<file>')[1].split('</file>')[0]
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="block"]/div/div/b')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Novamov":
		try:
			if LinkType == 4:
				VideoInfo = HTML.ElementFromURL(HostPage).xpath('//div[@id="content_block"]/div/center/script')[1].text
			if LinkType == 1:
				VideoInfo = HTML.ElementFromURL(HostPage).xpath('//body/script')[5].text
			try:
				CodeString = VideoInfo.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[2].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				VideoID = CharSrc.split('flashvars.file=')[1].split('"')[1]
				VideoKey = CharSrc.split('flashvars.filekey=')[1].split('"')[1]
			except:
				VideoID = VideoInfo.split('flashvars.file="')[1].split('"')[0]
				VideoKey = VideoInfo.split('flashvars.filekey="')[1].split('"')[0]
			url = "http://www.novamov.com/api/player.api.php?pass=undefined&cid=1&key="+VideoKey+"&cid2=undefined&cid3=undefined&file="+VideoID+"&numOfErrors=0&user=undefined"
			headers = {'User-Agent': UserAgent, 'Host': 'www.novamov.com', 'Referer': 'http://www.novamov.com/player/novamov-v5.swf'}
			session = requests.session()
			VideoInfo =  session.get(url, headers=headers)
			VideoStream = urllib.unquote(VideoInfo.content.split('=')[1].split('&')[0])
			if VideoStream == "1":
				InputError = VideoInfo.content.split('=')[2]
				if InputError == "Incorrect IP. Please refresh!!":
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongIP")
				else:
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == 'Nowveo':
		try:
			VideoPage = HostPage.split('file')[0]+"file1"+HostPage.split('file')[1]
			VideoInfo = HTML.ElementFromURL(VideoPage).xpath('//div[@id="main"]/div') 
			VideoStream = VideoInfo[3].xpath('./script[@type="text/javascript"]')[1].text.split('src: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Nowvideo":
		try:
			session = requests.session()
			headers = {'User-Agent': UserAgent, 'Host': 'www.nowvideo.sx', 'Referer': url}

			if LinkType == 4:
				VideoPage = session.get(HostPage, headers=headers)
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="content_player"]/table/tr/td/script')[1].text
			elif LinkType == 1:
				headers['Host'] = 'embed.nowvideo.sx'
				VideoPage = session.get(HostPage, headers=headers)
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//body/script')[5].text

			try:
				CodeString = VideoInfo.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[2].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				VideoID = CharSrc.split('flashvars.file="')[1].split('"')[0]
				FindVideoKey = urllib.quote(CharSrc.split('flashvars.filekey=')[1].split(';')[0])
				VideoKey = urllib.quote(CharSrc.split(FindVideoKey+'="')[1].split('"')[0])
			except:
				VideoID = VideoInfo.split('flashvars.file="')[1].split('"')[0]
				VideoKey = VideoInfo.split('fkzd="')[1].split('"')[0]

			headers['Host'] = 'www.nowvideo.sx'
			headers['Referer'] = 'http://embed.nowvideo.sx/player/nowvideo-v5.swf'
			url = "http://www.nowvideo.sx/api/player.api.php?pass=undefined&cid=undefined&key="+VideoKey+"1&cid2=undefined&file="+VideoID+"&cid3=undefined&numOfErrors=0&user=undefined"
			VideoInfo =  session.get(url, headers=headers)
			VideoStream = VideoInfo.content.split('=')[1].split('&')[0]
			if VideoStream == "1":
				InputError = VideoInfo.content.split('=')[2]
				if InputError == "Incorrect IP. Please refresh!!":
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongIP")
				else:
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Played":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'referer': HostPage})
			VideoStream = VideoPage.content.split('file: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Potlocker":
		try:
			VideoScr = HTML.ElementFromURL(HostPage).xpath('//div[@id="Playerholder"]/iframe')[0].get('src')
			VideoInfo = HTML.ElementFromURL(VideoScr).xpath('//div[@id="player_code"]/script')[1].text
			VideoStream = VideoInfo.split("file: '")[1].split("'")[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Primeshare":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, wait=8)
			VideoStream = VideoPage.content.split('<div id="player"')[1].split("clip: {")[1].split("url: '")[1].split("'")[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Project-free-upload":
		#project-free-upload.com
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			VideoInfo = VideoPage.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split("</script>")[0]
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Promptfile":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//body/script')[0].text.split("url: '")[1].split("'")[0]
				session = requests.session()
				session.cookies = VideoPage.cookies
				headers = {'User-Agent': UserAgent, 'Host': 'www.promptfile.com'}
				VideoID = session.head(VideoInfo, headers=headers)
				try:
					VideoStream = VideoID.headers['Location']
				except:
					VideoStream = ErrorMessage(Host=Host, LogError=1)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="not_found_msg"]')[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Putlocker":
		try:
			NS = {'media':'http://search.yahoo.com/mrss/'}
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'confirm': 'Continue as Free User'})
			try:
				VideoPageXML = "http://www.putlocker.com" + VideoPage.content.split("playlist: '")[1].split("'")[0]
				VideoInfo = XML.ElementFromURL(VideoPageXML)
				try:
					VideoStream = VideoInfo.xpath('//item/media:content', namespaces=NS)[1].get('url').replace('&amp;', '&')
				except:
					VideoStream = VideoInfo.xpath('//item/media:content', namespaces=NS)[0].get('url').replace('&amp;', '&')
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath("//div[@class='message t_0']")[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Putme":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"referer": url})
			VideoInfo = SecondButtonPress(url=HostPage, HostPage=HostPage, page=VideoPage, addkey={"referer": url})
			VideoID = VideoInfo.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split("</script>")[0]
			VideoURL = ScriptConvert(script=VideoID)
			cookies = {'ref_url': urllib.quote_plus(HostPage)}
			headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': 'http://putme.org/player6/StrobeMediaPlayback.swf'}
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Rocketfiles":
		try:
			VideoID = HostPage.split('/')[4]
			VideoPageXML = "http://flashvids.org/Xajax/saveaction/?xjxfun=load_player_eng&xjxr="+str(time.time())+"&xjxargs[]="+VideoID+"&xjxargs[]=N4"
			VideoStream = XML.ElementFromURL(VideoPageXML).xpath('//cmd')[0].text.split('&file=')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Royalvids":
		try:
			HostPage = "http://royalvids.eu/embed-" + HostPage.split('/')[4] + ".html"
			VideoPage = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script')[0].text
			VideoStream = ScriptConvert(script=VideoPage)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Safecloud":
		try:
			headers = {'User-Agent': UserAgent, 'Referer': url}
			session = requests.session()
			VideoPage = session.get(HostPage, headers=headers)
			VideoID = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="download"]/script')[1].text
			cookies = CookieDict(cookies=session.cookies)
			VideoURL = VideoID.split('flashvars.videoPath')[1].split('= "')[1].split('"')[0]
			headers['Referer'] = HostPage
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Sharerepo":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			VideoInfo = VideoPage.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split("</script>")[0]
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Sharesix":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'method_free': 'Free'})
			VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Sharevid":
		try:
			VideoPage = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script')[0].text
			VideoStream = ScriptConvert(script=VideoPage)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Skylo":
		try:
			VideoPage = "http://skylo.me/videos.php?Id="+HostPage.split('=')[1]
			VideoInfo = HTML.ElementFromURL(VideoPage).xpath('//div[@class="containerDiv"]/script')[1].text
			vidstr = 'mp4:' + VideoInfo.split("file','")[1].split("'")[0]
			swfurl = VideoInfo.split("SWFObject('")[1].split("'")[0]
			url_MO = int(swfurl.split('/')[3].split('.')[0])
			rtmpurl = ["", "rtmp://213.163.74.241/vod", "rtmp://213.163.74.225/vod", "rtmp://213.163.74.229/vod", "rtmp://213.163.74.233/vod", "rtmp://213.163.74.237/vod"]
			VideoStream = [vidstr, swfurl, rtmpurl[url_MO], 'rtmp', VideoPage, 'vod']
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Sockshare":
		try:
			NS = {'media':'http://search.yahoo.com/mrss/'}
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="play"]/script')[0].text.split("playlist: '")[1].split("',")[0]
				VideoPageXML = "http://www.sockshare.com" + VideoInfo
				VideoStream = XML.ElementFromURL(VideoPageXML).xpath('//item/media:content', namespaces=NS)[0].get('url').replace('&amp;', '&')
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="deleted"]')[0].text
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Stageflv":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, wform=1, addkey={"imhuman": "Proceed to video"})
			VideoStream = VideoPage.content.split("file: ")[1].split('"')[1]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Stream2k":
		try:
			headers = {'User-Agent': UserAgent, 'Referer': url}
			req = requests.get(HostPage, headers=headers)
			VideoStream = urllib.unquote(HTML.ElementFromString(req.content).xpath('//div[@id="player"]/object/param[@name="flashvars"]')[0].get('value').split('file=')[1].split('&')[0])
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=3)
	elif Host == "Stream2k.eu":
		try:
			session = requests.session()
			headers = {'User-Agent': UserAgent, 'Referer': url}
			s = session.get(HostPage, headers=headers)
			cookies = CookieDict(cookies=session.cookies)
			VideoID = "http://stream2k.eu/ajax.php?p=video&do=getplayer&vid="+HostPage.split('_')[1].split('.')[0]+"&aid=1&player=detail"
			headers['Referer'] = HostPage
			VideoInfo = session.get(VideoID, headers=headers)
			VideoURL = urllib.unquote(VideoInfo.content.split('file=')[1].split('&')[0])
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Streamme":
		try:
			VideoPage = "http://streamme.cc/playerframe.php?Id="+HostPage.split('/')[4]
			VideoInfo = HTML.ElementFromURL(VideoPage).xpath('//div[@class="containerDiv"]/script')[1].text
			vidstr = 'mp4:' + VideoInfo.split("file','")[1].split("'")[0]
			swfurl = VideoInfo.split("SWFObject('")[1].split("'")[0]
			url_MO = int(swfurl.split('/')[3].split('.')[0])
			rtmpurl = ["", "rtmp://213.163.74.241/vod", "rtmp://213.163.74.225/vod", "rtmp://213.163.74.229/vod", "rtmp://213.163.74.233/vod", "rtmp://213.163.74.237/vod"]
			VideoStream = [vidstr, swfurl, rtmpurl[url_MO], 'rtmp', VideoPage, 'vod']
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Streamcloud":
		try:
			cookies = {'age_ver': '1'}
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, cookies=cookies, wait=10, addkey={'referer': url})
			VideoURL = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text.split('file: "')[1].split('"')[0]
			headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': HostPage}
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=6)
	elif Host == "Streamvids":
		try:
			session = requests.session()
			headers = {'User-Agent': UserAgent, 'Referer': url}
			s = session.get(HostPage, headers=headers)
			cookies = CookieDict(cookies=session.cookies)
			VideoID = "http://streamvids.eu/ajax.php?p=video&do=getplayer&vid="+HostPage.split('_')[1].split('.')[0]+"&aid=1&player=detail"
			headers['Referer'] = HostPage
			VideoInfo = session.get(VideoID, headers=headers)
			VideoURL = urllib.unquote(VideoInfo.content.split('file=')[1].split('&')[0])
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Thefile":
		try:
			VideoInfo = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script[@type=\'text/javascript\']')[1].text
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=6)
	elif Host == "Tomwans":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player"]/div/video/source')[0].get('src')
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Tubecloud":
		try:
			cookies = {'ref_url': urllib.quote_plus(url)}
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, cookies=cookies, addkey={'referer': urllib.quote_plus(url), 'imhuman': 'Proceed+to+video'})
			VideoStream = VideoPage.content.split('file: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=3)
	elif Host == "Tudou":
		try:
			VideoPage = HTML.ElementFromURL(HostPage).xpath('//body/script')[0].text
			try:
				VideoID = "http://v2.tudou.com/v.action?it="+VideoPage.split('iid: ')[1].split(',')[0]
				VideoStream = XML.ElementFromURL(VideoID).xpath('//f')[0].text
			except:
				VideoID = "http://v0.tudou.com/v2/itudou?id="+VideoPage.split('iid: ')[1].split(',')[0]
				VideoStream = XML.ElementFromURL(VideoID).xpath('//f')[0].text
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Uncapped-downloads":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={'referer': url})
			VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Undergroundflix":
		try:
			VideoPage = HTML.ElementFromURL(HostPage).xpath("//div[@class='postTabs_divs postTabs_curr_div']/center/iframe")[0].get('src')
			Host = VideoPage.split('/')[2].split('.')[0].capitalize()
			if Host == 'Www' or Host == 'Embed':
				Host = VideoPage.split('/')[2].split('.')[1].capitalize()
			VideoStream = GetMovie(Host=Host, HostPage=VideoPage, url=url, LinkType=1)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)	
	elif Host == "Uploadc":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"method_free": "Slow access", "referer": url})
			VideoInfo = HTML.ElementFromString(VideoPage.content)
			try:
				VideoScript = VideoInfo.xpath('//div[@id="player_code"]/script')[0].text
				try:
					VideoStream = VideoScript.split("file','")[1].split("'")[0]
				except:
					VideoStream = ScriptConvert(script=VideoScript)
			except:
				InputError = VideoInfo.xpath('//div[@id="content"]//center//center')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Userporn":
		try:
			if LinkType == 4:
				VideoID = HostPage.split('=')[1]
			elif LinkType == 2:
				VideoID = HostPage.split('/')[4]

			url = "http://www.userporn.com/player_control/settings.php?v="+VideoID+"&em=TRUE&fv=v1.1.55"
			url2 = "http://www.userporn.com/player/player.swf?v="+VideoID+"&em=TRUE&sd=www.userporn.com"
			HOSTER_KEY1 = "NTI2NzI5Cgo="
			headers = {'User-Agent': UserAgent, 'Host': 'www.userporn.com', 'Referer': url2}
			cookies = {'UP_disclaim': '1'}
			session = requests.session()
			OpenUrl = session.get(url, headers=headers, cookies=cookies)
			VideoPage = OpenUrl.content.split('"token1":"')[1].split('"')[0].decode('base64', 'strict')
			KeyString = OpenUrl.content.split('"time":"')[1].split('"')[0]
			KeyOne = int(OpenUrl.content.split('"rkts":')[1].split(',')[0])
			KeyTwo = int(HOSTER_KEY1.decode('base64', 'strict'))
			VideoKey = zDecrypt(KeyString, KeyOne, KeyTwo, 82, 84669, 48779, 32, 65598, 115498)
			VideoURL = VideoPage+"&c="+VideoKey+"&start=0"
			cookies.update(CookieDict(cookies=session.cookies))
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "V-vids":
		try:
			if LinkType == 4:
				HostPage = "http://v-vids.com/embed-" + HostPage.split('/')[3] + "-640x360.html"
			VideoPage = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script')[1].text
			VideoStream = VideoPage.split("file: '")[1].split("'")[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Veehd":
		try:
			headers = {'User-Agent': UserAgent, 'Host': 'veehd.com'}
			session = requests.session()
			VideoPage = session.get(HostPage, headers=headers)
			try:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="contentColumnLeft"]//a/div/b')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
			except:
				VideoPage = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="main"]/script')[1].text
				VideoURL = "http://veehd.com"+VideoPage.split('src : "')[1].split('"')[0]
				VideoInfo = session.get(VideoURL, headers=headers)
				VideoStream = urllib.unquote(HTML.ElementFromString(VideoInfo.content).xpath('//object[@id="veehdplayer"]/param[@name="flashvars"]')[0].get('value').split('url":"')[1].split('"')[0])

		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Veevr":
		try:
			headers = {'User-Agent': UserAgent, 'Host': 'veevr.com'}
			session = requests.session()
			VideoPage = session.get(HostPage, headers=headers)
			try:
				cookies = CookieDict(cookies=session.cookies)
				vidID = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_cont"]/script')[1].text
				VideoURL = vidID.split('clip: {')[1].split("url: '")[1].split("'")[0]
				VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="not_found_404_page"]/div')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=8, ErrorType="HostDown")
	elif Host == "Veervid":
		try:
			VideoPage = HostPage.split('file')[0]+"file1"+HostPage.split('file')[1]
			VideoStream = HTML.ElementFromURL(VideoPage).xpath('//form')[0].get('action')
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Vidbull":
		try:
			if LinkType == 4:
				HostPage = "http://vidbull.com/embed-"+HostPage.split('/')[3].split('.')[0]+"-640x318.html"
			VideoPage = HTML.ElementFromURL(HostPage)
			try:
				VideoInfo = VideoPage.xpath('//div[@id="player_code"]/script')[2].text
				VideoStream = ScriptConvert(script=VideoInfo)
			except:
				InputError = VideoPage.xpath('//body/div/span')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidbox":
		try:
			if LinkType == 4:
				if HostPage.split('/')[2] == "vidbox.eu":
					HostPage = "http://vidbox.eu/embed-"+HostPage.split('/')[3].split('.')[0]+"-640x318.html"
				elif HostPage.split('/')[2] == "vidbox.yt":
					HostPage = "http://vidbox.yt/embed-"+HostPage.split('/')[3]+"-640x318.html"
			VideoPage = HTML.ElementFromURL(HostPage)
			try:
				try:
					#Vidbox.eu
					VideoInfo = VideoPage.xpath('//div[@id="player_code"]/script')[0].text
					VideoStream = ScriptConvert(script=VideoInfo)
				except:
					#Vidbox.yt
					VideoInfo = VideoPage.xpath('//body/script')[0].text
					VideoStream = VideoInfo.split("playlist:")[5].split("url: '")[2].split("'")[0]
			except:
				try:
					InputError = VideoPage.xpath('//div[@class="xxc"]/h3')[0].text.strip()
				except:
					InputError = VideoPage.text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidbux" or Host == "Vidbux_2":
		try:
			if Host == "Vidbux":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host)
			elif Host == "Vidbux_2":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=2)

			try:
				VideoScript = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="embedcontmvshre"]/script')[0].text
				VideoStream = ScriptConvert(script=VideoScript)
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="clearfix content_mainbody"]/center/div/p/b')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
				except:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="clearfix content_mainbody"]/center/div/p')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")

			if Host == "Vidbux":
				VOID = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=1)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Videohub":
		try:
			if LinkType == 4:
				HostPage = "http://videohub.ws/videos.php?Id="+HostPage.split('=')[1]
			VideoInfo = HTML.ElementFromURL(HostPage).xpath('//div[@class="containerDiv"]/script')[1].text
			vidstr = VideoInfo.split("file','")[1].split("'")[0]
			swfurl = "mp4:" + VideoInfo.split("SWFObject('")[1].split("'")[0]
			rtmpurl = "rtmp://93.115.92.168:1"
			app = ""
			VideoStream = [vidstr, swfurl, rtmpurl, 'rtmp', HostPage, app]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Videoize":
		try:
			VideoPage = HTML.ElementFromURL(HostPage)
			try:
				VideoInfo = VideoPage.xpath('//div[@id="player"]/script')[1].text
				VideoStream = ScriptConvert(script=VideoInfo)
			except:
				InputError = VideoPage.xpath('//div[@class="title"]')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Videomega":
		try:
			VideoPage = HTML.ElementFromURL(HostPage).xpath('//div[@class="embed"]')[1]
			VideoID = VideoPage.xpath('./div')[0].text.split('src="')[1].split('"')[0]
			VideoInfo = HTML.ElementFromURL(VideoID).xpath('//body/script[@type="text/javascript"]')[0].text.split('unescape("')[1].split('"')[0]
			VideoStream = urllib.unquote(VideoInfo).split('file: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Videopluz":
		try:
			VideoStream = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script')[1].text.split('file: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Videopremium":
		try:
			try:
				session = requests.session()
				cookies = {}
				headers = {'User-Agent': UserAgent, 'Referer': url}
				s = session.get(HostPage, headers=headers)
				cookies.update(CookieDict(cookies=session.cookies))
				HostPage = HTML.ElementFromString(s.content).xpath('//head/script')[0].text.split("window.location = '")[1].split("'")[0]
			except:
				pass
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, cookies=cookies, addkey={"referer": url})
			try:					
				VideoScript = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[2].text
				VideoStream = ScriptConvert(script=VideoScript)			
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="middle-cont"]/h1')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Videoslasher":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				VideoInfo = "http://www.videoslasher.com" + HTML.ElementFromString(VideoPage.content).xpath('//div[@class="wrapper"]/div/script')[1].text.split("playlist: '")[1].split("'")[0]
				headers = {'User-Agent': UserAgent, 'Referer': HostPage}
				session = requests.session()
				session.cookies = VideoPage.cookies
				VideoID = session.get(VideoInfo, headers=headers)
				VideoURL = VideoID.content.split('url="')[2].split('"')[0]
				cookies = CookieDict(cookies=session.cookies)
				VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = VideoPage.content.split('<div>')[1].split('</div>')[0]
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Videoweed":
		try:
			VideoPage = HTML.ElementFromURL(HostPage)

			try:
				if LinkType == 4:
					VideoInfo = VideoPage.xpath('//div[@id="player_block_ads"]/script[@type="text/javascript"]')[1].text
				elif LinkType == 1:
					VideoInfo = VideoPage.xpath('//body/script[@type="text/javascript"]')[5].text

				CodeString = VideoInfo.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[1].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				CodeString = CharSrc.split("eval")[2].split(";}('")[1].split("'));")[0]
				CharSrc = CharConvert(w=CodeString.split("','")[0],i=CodeString.split("','")[1],s=CodeString.split("','")[2],e=CodeString.split("','")[3])
				VideoID = CharSrc.split('flashvars.file=')[1].split('"')[1]
				VideoKey = CharSrc.split('flashvars.filekey=')[1].split('"')[1]
			except:
				if LinkType == 4:
					VideoInfo = VideoPage.xpath('//div[@id="player_block_ads"]/script[@type="text/javascript"]')[2].text
				elif LinkType == 1:
					VideoInfo = VideoPage.xpath('//body/script[@type="text/javascript"]')[5].text

				VideoID = VideoInfo.split('flashvars.file="')[1].split('"')[0]
				VideoKey = VideoInfo.split('flashvars.filekey="')[1].split('"')[0]

			url = "http://www.videoweed.es/api/player.api.php?file="+VideoID+"&user=undefined&key="+VideoKey+"&cid3=undefined&numOfErrors=0&cid=1&cid2=undefined&pass=undefined"
			headers = {'User-Agent': UserAgent, 'Host': 'www.videoweed.es', 'Referer': 'http://www.videoweed.es/player/videoweed-v5.swf'}
			session = requests.session()
			VideoInfo =  session.get(url, headers=headers)
			VideoStream = VideoInfo.content.split('=')[1].split('&')[0]
			if VideoStream == "1":
				InputError = VideoInfo.content.split('=')[2]
				if InputError == "Incorrect IP. Please refresh!!":
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongIP")
				else:
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Videozed":
		#Ilivid Player plugin
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"referer": url})
			try:
				cookies = CookieDict(cookies=VideoPage.cookies)
				VideoInfo = SecondButtonPress(url=HostPage, HostPage=HostPage, page=VideoPage, cookies=cookies, addkey={"method_premium":"", "referer": HostPage})
				VideoID = HTML.ElementFromString(VideoInfo.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoURL = ScriptConvert(script=VideoID)
				cookies = {'ref_url': urllib.quote_plus(HostPage)}
				headers = {'User-Agent': UserAgent[UserAgentNum], 'Host': VideoURL.split('/')[2], 'Referer': 'http://videozed.net/player/player.swf'}
				VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="content_mdl"]/div/h3')[0].text.strip() + " - Video has been removed"
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidhog":
		try:
			headers = {'User-Agent': UserAgent, 'Referer': HostPage}
			session = requests.session()
			VideoPage = session.get(HostPage, headers=headers)
			cookies = CookieDict(cookies=session.cookies)
			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//font[@color="red"]')[0].text.split('.')
				VideoID = 'http://vidhog.com/vidembed-' + HostPage.split('/')[3] + '.' + VideoInfo[-1]
				VideoURL = session.head(VideoID, headers=headers)
				VideoStream = VideoURL.headers['location'] + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="content-bg"]/h3')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidplay" or Host == "Vidplay_2":
		try:
			if LinkType == 4:
				HostPage = "http://vidplay.net/embed-"+HostPage.split('/')[3]+"-640x360.html"
		
			if Host == "Vidplay":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host)
			elif Host == "Vidplay_2":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=2)

			try:
				VideoScript = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoStream = ScriptConvert(script=VideoScript)
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="clearfix content_mainbody"]/center/div/p/b')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
				except:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="clearfix content_mainbody"]/center/div/p')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")

			if Host == "Vidplay":
				VOID = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=1)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=4)
	elif Host == "Vidspot":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[3].text.split('"playlist" :')[1].split('"file" : "')[1].split('"')[0]
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="content"]/b')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidstream":
		try:
			if LinkType == 4:
				HostPage = "http://vidstream.in/embed-" + HostPage.split('/')[3] + "-720x480.html"
			VideoPage = HTML.ElementFromURL(HostPage)
			try:
				VideoStream = VideoPage.xpath('//div[@id="player_code"]/script[@type=\'text/javascript\']')[1].text.split('file: "')[1].split('"')[0] + "?start=0"
			except:
				InputError = VideoPage.text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidto":
		if LinkType == 4:
			HostPage = "http://vidto.me/embed-"+HostPage.split('/')[3].split('.')[0]+"-640x340.html"
		try:
			VideoPage = HTML.ElementFromURL(HostPage)
			try:
				VideoInfo = VideoPage.xpath('//div[@id="player_code"]/script')[2].text
				VideoStream = ScriptConvert(script=VideoInfo)
			except:
				InputError = VideoPage.xpath('//span[@class="deleted"]')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidup":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				try:
					VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
				except:
					VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[0].text
				VideoStream = ScriptConvert(script=VideoInfo)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="content"]/b')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidx":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, wait=10)
			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
				VideoURL = VideoInfo.split('file: "')[1].split('"')[0]
				cookies = {'ref_url': url}
				headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': url}
				VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//section[@id="content"]/div')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vidxden" or Host == "Vidxden_2":
		try:
			if Host == "Vidxden":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host)
			elif Host == "Vidxden_2":
				VideoPage = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=2)

			try:
				VideoScript = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="embedcontmvshre"]/script')[0].text
				VideoStream = ScriptConvert(script=VideoScript)
			except:
				try:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="clearfix content_mainbody"]/center/div/p/b')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
				except:
					InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@class="clearfix content_mainbody"]/center/div/p')[0].text.strip()
					VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="WrongCaptcha")

			if Host == "Vidxden":
				VOID = SolveMediaCaptcha(url=url, HostPage=HostPage, Host=Host, RecaptchaResponse=1)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vodlocker":
		try:
			if LinkType == 4:
				HostPage = "http://vodlocker.com/embed-"+HostPage.split('/')[3]+"-640x360.html"

			headers = {'User-Agent': UserAgent, 'Referer': url}
			session = requests.session()
			VideoPage = session.get(HostPage, headers=headers)
			try:
				VideoInfo = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[1].text
				try:
					swfurl = "http://vodlocker.com/player/player.swf"
					vidstr = VideoInfo.split('file: "')[1].split('"')[0]
					rtmpurl = VideoInfo.split('streamer: "')[1].split('"')[0]
					app = VideoInfo.split('streamer: "')[1].split('"')[0].split('/')[3]
					VideoStream = [vidstr, swfurl, rtmpurl, 'rtmp', HostPage, app]
				except:
					VideoStream = VideoInfo.split('file: "')[1].split('"')[0]
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//span')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vreer":
		try:
			if LinkType == 4:
				HostPage = "http://vreer.com/embed-" + HostPage.split('/')[3] + "-960x481.html"
			headers = {'User-Agent': UserAgent, 'Host': 'veevr.com'}
			session = requests.session()
			VideoPage = session.get(HostPage, headers=headers)
			try:
				cookies = CookieDict(cookies=session.cookies)
				vidID = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="player_code"]/script')[2].text
				VideoURL = vidID.split('file: "')[1].split('"')[0]
				VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
			except:
				InputError = VideoPage.content.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Vureel":
		try:
			url = "http://www.vureel.com/playwire.php?vid=" + HostPage.split('/')[4]
			headers = {'User-Agent': UserAgent, 'Content-Type': 'text/xml', 'Host': 'www.vureel.com', 'Origin': 'http://www.vureel.com', 'Referer': HostPage}
			VideoInfo =  requests.get(url, headers=headers)
			VideoStream = VideoInfo.content.split('<src>')[1].split('</src>')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Watchfreeinhd":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage)
			try:
				VideoStream = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="playerHolder"]/a[@id="player"]')[0].get('href')
			except:
				InputError = HTML.ElementFromString(VideoPage.content).xpath('//div[@id="content"]/div/div')[1].text_content().strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Wupfile":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"referer": url})
			VideoInfo = VideoPage.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split('</script>')[0]
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Xvidstage":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"referer": url})
			VideoInfo = VideoPage.content.split('<div id="player_code">')[1].split("<script type='text/javascript'>")[1].split('</script>')[0]
			VideoStream = ScriptConvert(script=VideoInfo)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Yamivideo":
		try:
			VideoID = HostPage.split('/')[4]
			VideoPageXML = "http://yamivideo.com/Xajax/saveaction/?xjxfun=load_player_eng&xjxr="+str(time.time())+"&xjxargs[]="+VideoID+"&xjxargs[]=N1"
			VideoStream = XML.ElementFromURL(VideoPageXML).xpath('//cmd')[0].text.split('&file=')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Yesload":
		if LinkType == 1:
			url = "http://yesload.net/player_api/info?token="+HostPage.split('/')[3]+"&user="
		elif LinkType == 3:
			url = "http://yesload.net/player_api/info?token="+HostPage.split('/')[3].split('?')[0]+"&user="
		try:
			headers = {'User-Agent': UserAgent}
			VideoInfo =  requests.get(url, headers=headers)
			VideoStream = VideoInfo.content.split('=')[1].split('&')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Youwatch":
		try:
			if LinkType == 4:
				HostPage = "http://youwatch.org/embed-"+HostPage.split('/')[3]+"-720x480.html"
			VideoStream = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script[@type=\'text/javascript\']')[1].text.split('file: "')[1].split('"')[0]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Zalaa":
		try:
			VideoPage = SecondButtonPress(url=url, HostPage=HostPage, addkey={"method_free": "Slow access", "referer": url})
			VideoInfo = HTML.ElementFromString(VideoPage.content)
			try:
				VideoScript = VideoInfo.xpath('//div[@id="player_code"]/script')[0].text
				try:
					VideoStream = VideoScript.split("file','")[1].split("'")[0]
				except:
					VideoStream = ScriptConvert(script=VideoScript)
			except:
				InputError = VideoInfo.xpath('//div[@id="content"]//center//center')[0].text.strip()
				VideoStream = ErrorMessage(Host=Host, InputError=InputError, ErrorType="VideoRemoved")
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1, ErrorType="HostDown")
	elif Host == "Zinwa":
		try:
			VideoInfo = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script')[1].text
			ScriptEncode = VideoInfo.split("eval(decodejs('")[1].split("'")[0].split(",")
			VideoDecode = ''.join(map(unichr, map(int, ScriptEncode)))
			VideoPage = VideoDecode.split('"link": "')[1].split('"')[0]
			vidstr = VideoDecode.split("'hq' : '")[1].split("'")[0]
			swfurl = "http://www.zinwa.com/zinwa/player.swf"
			rtmpurl = VideoDecode.split('streamer: "')[1].split('"')[0]
			app = VideoDecode.split('streamer: "')[1].split('"')[0].split('/')[3]
			VideoStream = [vidstr, swfurl, rtmpurl, 'rtmp', VideoPage, app]
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	elif Host == "Zooupload":
		VideoStream = ErrorMessage(Host=Host, LogError=3, ErrorType="HostDown")
	elif Host == "Zuzvideo":
		try:
			VideoURL = HTML.ElementFromURL(HostPage).xpath('//div[@id="player_code"]/script')[1].text.split('file: "')[1].split('"')[0]
			cookies = {'lang': 'english'}
			headers = {'User-Agent': UserAgent, 'Host': VideoURL.split('/')[2], 'Referer': 'http://zuzvideo.com/player/player.swf'}
			VideoStream = VideoURL + "?cookies="+String.Quote(str(cookies), usePlus=True)+"&headers="+String.Quote(str(headers), usePlus=True)
		except:
			VideoStream = ErrorMessage(Host=Host, LogError=1)
	else:
		VideoStream = ErrorMessage(Host=Host, LogError=7, ErrorType="HostDown")

	return VideoStream