####################################################################################################
# Setting up imports

import inspect, os, sys
try:
	path = os.getcwd().split("?\\")[1].split('Plug-in Support')[0]+"Plug-ins\MOVIE2K.bundle\Contents\Services\URL\MOVIE2K\Modules"
except:
	path = os.getcwd().split("Plug-in Support")[0]+"Plug-ins/MOVIE2K.bundle/Contents/Services/URL/MOVIE2K/Modules"
	
if path not in sys.path:
    sys.path.append(path)

try:
	import requests
except:
	import requests25 as requests

import simplejson
import demjson
import urllib
import urllib2
import time
import re

from OCR import GetImgValue
from ordereddict import OrderedDict

CAPTCHA_DATA = 'captcha.data.json'


####################################################################################################
#The JSON file is read/saved in the data cache for this plugin setup by Plex
def JsonOpen(fp):
	ParentalPassword = ""

	if os.path.exists(fp) == False:
		CaptchaData = JsonStruct(fp=fp, ParentalPassword=ParentalPassword, GetVersion=Version)
	else:
		f = open(fp, "rb")
		CaptchaData = f.read()
		f.close()

	try:
		SystemData = LoadData(fp=fp, Data=CaptchaData, LoadFile=False)
		if Version != SystemData[0][1]['Version']:
			ParentalPassword = SystemData[0][1]['ParentalPassword']
			CaptchaData = JsonStruct(fp=fp, ParentalPassword=ParentalPassword, GetVersion=Version)
	except:
		CaptchaData = JsonStruct(fp=fp, ParentalPassword=ParentalPassword, GetVersion=Version)

	return CaptchaData


####################################################################################################
#The JSON file is saved in the data cache for this plugin setup by Plex
def JsonStruct(fp, ParentalPassword, GetVersion):
	jsondata = '[\n'
	jsondata = jsondata + '{1 : {host: "System", ParentalPassword: "'+ParentalPassword+'", Version:"'+GetVersion+'"}},\n'
	jsondata = jsondata + '{2 : {host: "180upload", url: "",  HostPage: "", page: "", adcopy_challenge: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{3 : {host: "Clicktoview", url: "", HostPage: "", page: "", recaptcha_challenge_field: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{4 : {host: "Fileloby", url: "",  HostPage: "", page: "", adcopy_challenge: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{5 : {host: "Grifthost", url: "", HostPage: "", page: "", recaptcha_challenge_field: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{6 : {host: "Lemuploads", url: "", HostPage: "", page: "", recaptcha_challenge_field: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{7 : {host: "Megarelease", url: "", HostPage: "", page: "", recaptcha_challenge_field: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{8 : {host: "Vidbux", url: "",  HostPage: "", page: "", adcopy_challenge: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{9 : {host: "Vidplay", url: "",  HostPage: "", page: "", adcopy_challenge: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{10 : {host: "Vidxden", url: "",  HostPage: "", page: "", adcopy_challenge: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}}\n'
	jsondata = jsondata + ']'
	
	JsonWrite(fp=fp, jsondata=jsondata)

	return jsondata


####################################################################################################
#The JSON file is read/saved in the data cache for this plugin setup by Plex
def JsonFavoriteOpen(fp):
	if os.path.exists(fp) == False:
		FavoritesData = JsonFavoriteStruct(fp=fp)
	else:
		f = open(fp, "rb")
		FavoritesData = f.read()
		f.close()

	return FavoritesData


####################################################################################################
#The JSON file is saved in the data cache for this plugin setup by Plex
def JsonFavoriteStruct(fp):
	jsondata = '[\n'
	jsondata = jsondata + '{1 : {SiteURL: "", ThumbURL: "", Title: "", Summary:"", Date: ""}},\n'
	jsondata = jsondata + ']'
	
	JsonWrite(fp=fp, jsondata=jsondata)

	return jsondata


####################################################################################################
#The JSON file is read/saved in the data cache for this plugin setup by Plex
def JsonWatchLaterOpen(fp):
	if os.path.exists(fp) == False:
		FavoritesData = JsonWatchLaterStruct(fp=fp)
	else:
		f = open(fp, "rb")
		FavoritesData = f.read()
		f.close()

	return FavoritesData


####################################################################################################
#The JSON file is saved in the data cache for this plugin setup by Plex
def JsonWatchLaterStruct(fp):
	jsondata = '[\n'
	jsondata = jsondata + '{1 : {Type: "", Path: "", Host: "", DateAdded: "", Quality: "", ThumbURL: "", Title: "", Summary:"", Genres: "", Directors: "", GuestStars: "", Duration: "None", Rating: "0.0", Index: "0", Season: "0", ContentRating: "", SourceTitle: "", Date: "", VideoType: "", VideoStreamLink: "", HostPage: "", URL: "", LinkType: "", ContentLength: "", FileCheckSize: "0", ResumePath: [], ResumeContentLength: "", ResumeCount: "0", Thread: "", FailedFileDeletion: ""}},\n'
	jsondata = jsondata + ']'
	
	JsonWrite(fp=fp, jsondata=jsondata)

	return jsondata


####################################################################################################
#The JSON file is saved in the data cache for this plugin setup by Plex
def JsonWrite(fp, jsondata):
	f = open(fp, "w+")
	f.write(str(jsondata).replace(", u'", ", '").replace(": u'", ": '").replace("{u'", "{'").replace("}},", "}},\n").replace("[", "[\n ").replace("]", "\n]").replace("[\n u'", "['").replace("[\n '", "['").replace("'\n]", "']"))
	f.close()

	return True


####################################################################################################
# This function loads the json data file
def LoadData(fp, Data=None, LoadFile=True, GetJson=1):
	if LoadFile:
		if GetJson == 1:
			Data = JsonOpen(fp=fp)
		elif GetJson == 2:
			Data = JsonFavoriteOpen(fp=fp)
		elif GetJson == 3:
			Data = JsonWatchLaterOpen(fp=fp)

	try:
		obj = simplejson.loads(Data)
	except:
		obj = demjson.decode(Data)

	return obj


####################################################################################################
def StripArray(arraystrings):

	temparraystring = []
	
	for array_elem in arraystrings:
		elem = re.sub("[\n\t\xa0]", "", array_elem).strip()
		temparraystring.append(elem)

	return temparraystring


####################################################################################################
def ScriptConvert(script):
	Log(script)
	try:
		parameters = script.split(";',")
		CKtable = int(parameters[1].split(',')[0])
	except:
		parameters = script.split("}',")
		CKtable = int(parameters[1].split(',')[0])

	k = parameters[1].split(",'")[1].split("'.")[0].split('|')
	c = int(parameters[1].split(',')[1])
	p = parameters[0].split('return p}')[1].replace("\\", "")

	if CKtable <= 36:
		table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','10','11','12','13','14','15','16','17','18','19','1a','1b','1c','1d','1e','1f','1g','1h','1i','1j','1k','1l','1m','1n','1o','1p','1q','1r','1s','1t','1u','1v','1w','1x','1y','1z','20','21','22','23','24','25','26','27','28','29','2a','2b','2c','2d','2e','2f','2g','2h','2i','2j','2k','2l','2m','2n','2o','2p','2q','2r','2s','2t','2u','2v','2w','2x','2y','2z','30','31','32','33','34','35','36','37','38','39','3a','3b','3c','3d','3e','3f','3g','3h','3i','3j','3k','3l','3m','3n','3o','3p','3q','3r','3s','3t','3u','3v','3w','3x','3y','3z','40','41','42','43','44','45','46','47','48','49']
	elif CKtable <= 62:
		table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','10','11','12','13','14','15','16','17','18','19','1a','1b','1c','1d','1e','1f','1g','1h','1i','1j','1k','1l','1m','1n','1o','1p','1q','1r','1s','1t','1u','1v','1w','1x','1y','1z','1A','1B','1C','1D','1E','1F','1G','1H','1I','1J','1K','1L','1M','1N','1O','1P','1Q','1R','1S','1T','1U','1V','1W','1X','1Y','1Z','20','21','22','23','24','25','26','27','28','29','2a','2b','2c','2d','2e','2f','2g','2h','2i','2j','2k','2l','2m','2n','2o','2p','2q','2r','2s','2t','2u','2v','2w','2x','2y','2z','2A','2B','2C','2D','2E','2F','2G','2H','2I','2J','2K','2L','2M','2N','2O','2P','2Q','2R','2S','2T','2U','2V','2W','2X','2Y','2Z','30','31','32','34','35','36','37','38','39','3a','3b','3c','3d','3e','3f','3g','3h','3i','3j','3k','3l','3m','3n','3o','3p','3q','3r','3s','3t','3u','3v','3w','3x','3y','3z','3A','3B','3C','3D','3E','3F','3G','3H','3I','3J','3K','3L','3M','3N','3M','3O','3P','3Q','3R','3S','3T','3U','3V','3W','3X','3Y','3Z','40','41','42','43','44','45','46','47','48','49','4a','4b','4c','4d','4e','4f','4g','4h','4i','4j','4k','4l','4m','4n','4o','4p','4q','4r','4s','4t','4u','4v','4w','4x','4y','4z']

	while c >= 0:
		c = c - 1
		if k[c] != "":
			p = re.sub(r'\b'+table[c]+r'\b', k[c], p)
	Log(p)
	try:
		try:
			try:
				try:
					p = p.split('name="src"value="')[1].split('"')[0]
				except:
					p = p.split('name="src" value="')[1].split('"')[0]
			except:
				try:
					p = p.split("file','")[1].split("'")[0]
				except:
					VarArray = p.split('var ')
					try:
						VideoKeyVar = VarArray[len(VarArray)-16].split('=')[1].split(';')[0]
						p = p.split(VideoKeyVar)[1].split('="')[1].split('"')[0]
					except:
						VideoKeyVar = VarArray[len(VarArray)-17].split('=')[1].split(';')[0]
						p = p.split(VideoKeyVar)[1].split('="')[1].split('"')[0]
		except:			
			try:
				p = p.split('file:"')[1].split('"')[0]
			except:
				p = p.split("file':'")[1].split("'")[0]
	except:
		try:
			try:
				p = p.split('file":"')[1].split('"')[0]
			except:
				p = p.split('value="src=')[1].split('&')[0]
		except:
			try:
				p = p.split("file:'")[1].split("'")[0]
			except:
				p = p.split("clip:{url:'")[1].split("'")[0]
		
	Log(p)
	return p


####################################################################################################
def ScriptDecode(url):

	Host = url.split('/')[2]
	txdata = None
	txheaders = {'User-Agent': UserAgent, 'Referer': url}
	req = urllib2.Request(url, txdata, txheaders)
	OpenUrl =  urllib2.urlopen(req)
	script = OpenUrl.read().split('<script language=javascript>')[1].split('</script>')[0]
	OpenUrl.close()

	c = script.split('c="')[1].split('"')[0]
	d = ""

	for i, g in enumerate(c):
		if i%3 == 0:
			d = d + "%"
		else:
			d = d + g

	d = urllib.unquote(d)

	x = script.split('x("')[1].split('")')[0]
	l = len(x)
	t = d.split("t=Array(")[1].split(")")[0].split(",")
	s = 0
	w = 0
	r = ""
	
	for i, p in enumerate(x):
		w = w|(int(t[ord(p)-48])<<s)
		if s != 0:
			r =  r + chr(165^w&255);
			w = w >> 8
			s = s - 2
		else:
			s = 6

	return r


####################################################################################################
def zDecrypt(cipher, keyOne, keyTwo, arg0, arg1, arg2, arg3, arg4, arg5):	
	x = 0
	y = 0
	B = []

	result = ""
	i = 0
	while i < len(cipher):
		result = result + convertStr2Bin(cipher[i])
		i += 1
	
	C = list(result)
	longitud = len(C) * 2

	i = 0
	while i < longitud * 1.5:
		keyOne = ((keyOne * arg0) + arg1) % arg2
		keyTwo = ((keyTwo * arg3) + arg4) % arg5
		B.append((keyOne + keyTwo) % (longitud / 2))
		i += 1
  
	i = longitud
	while i >= 0:
		x = B[i]
		y = i % (longitud / 2)
		z = C[x]
		C[x] = C[y]
		C[y] = z
		i = i - 1

	i = 0
	while i < longitud/2:
		C[i] = str(int(C[i]) ^ (B[i + longitud] & 1))
		i += 1

	result = ""
	CC = ""
	CC = CC.join(C)
	i = 0
	while i < len(CC):
		result = result + convertBin2Str(CC[i:i+4])
		i = i + 4

	return result


####################################################################################################
def convertBin2Str(s):
	if s == "0000":
		dev = "0"
	elif s == "0001":
		dev = "1"
	elif s == "0010":
		dev = "2"
	elif s == "0011":
		dev = "3"
	elif s == "0100":
		dev = "4"
	elif s == "0101":
		dev = "5"
	elif s == "0110":
		dev = "6"
	elif s == "0111":
		dev = "7"
	elif s == "1000":
		dev = "8"
	elif s == "1001":
		dev = "9"
	elif s == "1010":
		dev = "a"
	elif s == "1011":
		dev = "b"
	elif s == "1100":
		dev = "c"
	elif s == "1101":
		dev = "d"
	elif s == "1110":
		dev = "e"
	elif s == "1111":
		dev = "f"

	return dev


####################################################################################################
def convertStr2Bin(s):
	if s == "0":
		result = "0000"
	elif s == "1":
		result = "0001"
	elif s == "2":
		result = "0010"
	elif s == "3":
		result = "0011"
	elif s == "4":
		result = "0100"
	elif s == "5":
		result = "0101"
	elif s == "6":
		result = "0110"
	elif s == "7":
		result = "0111"
	elif s == "8":
		result = "1000"
	elif s == "9":
		result = "1001"
	elif s == "a":
		result = "1010"
	elif s == "b":
		result = "1011"
	elif s == "c":
		result = "1100"
	elif s == "d":
		result = "1101"
	elif s == "e":
		result = "1110"
	elif s == "f":
		result = "1111"

	return result


####################################################################################################
def decodeurl(encodedurl):
    #encodedurl = "174917781793179d171e172d1762185c189418cd191b19a619d41a821ac11b331b1a1c551cfe1d991e2a1ee11f7f1f9f20fe21eb22bc22de24752554259f275d2848296c2a8d2b9a2c062df02e63301831a13238345335533643380339943ab33cbd3e163f9240f042ba44c2465047ee49574b494da04eee512352fc5547572e594d5b2b5d985f4161af63f565f968576a9b6c896f56714b73da75f278267b0f5628"
    tempp9 =""
    tempp4="1071045098811121041051095255102103119"
    strlen = len(encodedurl)
    temp5=int(encodedurl[strlen-4:strlen],10)
    Log(temp5)
    encodedurl=encodedurl[0:strlen-4]
    strlen = len(encodedurl)
    temp6=""
    temp7=0
    temp8=0
    while temp8 < strlen:
        temp7=temp7+2
        temp9=encodedurl[temp8:temp8+4]
        temp9i=int(temp9,16)
        partlen = ((temp8 / 4) % len(tempp4))
        partint=int(tempp4[partlen:partlen+1])
        temp9i=((((temp9i - temp5) - partint) - (temp7 * temp7)) -16)/3
        temp9=chr(temp9i)
        temp6=temp6+temp9
        temp8=temp8+4

    return temp6


####################################################################################################
def CharConvert(w,i,s,e):

	lIll = 0
	ll1I = 0
	Il1l = 0
	ll1l = []
	l1lI = []
	looper = True

	while looper == True:
		if lIll < 5:
			l1lI.append(w[lIll])
  		elif lIll < len(w):
			ll1l.append(w[lIll])
	  	lIll += 1
		if ll1I < 5:
			l1lI.append(i[ll1I])
		elif ll1I < len(i):
			ll1l.append(i[ll1I])
		ll1I += 1
		if Il1l < 5:
			l1lI.append(s[Il1l])
		elif Il1l < len(s):
			ll1l.append(s[Il1l])
		Il1l += 1
  		if len(w)+len(i)+len(s)+len(e) == len(ll1l)+len(l1lI)+len(e):
			looper = False

	lI1l = ''.join(ll1l)
	I1lI = ''.join(l1lI)
	ll1I = 0
	l1ll = []

	for lIll in range(0, len(ll1l), 2):
		ll11 = -1
		if ord(I1lI[ll1I])%2 == 1:
			ll11 = 1
		l1ll.append(chr(int(lI1l[lIll:lIll+2],36)-ll11))
		ll1I += 1
		if ll1I >= len(l1lI):
			ll1I = 0

	return ''.join(l1ll)


##################################################################################################################
def SecondButtonPress(url, HostPage, page=None, elm="", elm2="", wform=0, addkey=None, removekey=None, cookies={}, wait=0, captchakey=None, captchaimg=None, captchacookies={}, split=None, GetUserAgent=None):

	domain = HostPage.split('/')[2]
	payload = OrderedDict()
	headers = OrderedDict()
	headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
	headers['Accept-Encoding'] = 'gzip,deflate,sdch'
	headers['Accept-Language'] = 'en-US,en;q=0.8'
	headers['Cache-Control'] = 'max-age=0'
	headers['Connection'] = 'keep-alive'
	headers['Referer'] = url
	if GetUserAgent == None:
		headers['User-Agent'] = UserAgent
	else:
		headers['User-Agent'] = GetUserAgent

	session = requests.session()
	requests.utils.add_dict_to_cookiejar(session.cookies, cookies)


	if page != None:
		s = page
	else:
		s = session.get(HostPage, headers=headers)

	try:
		form = HTML.ElementFromString(s.content)
	except:
		form = HTML.ElementFromString(s)

	try:
		whichform = form.xpath('//'+elm+'form')[wform]
	
		if len(whichform.xpath('./'+elm2+'input')) != 0:
			for input in whichform.xpath('./'+elm2+'input'):
				if input.get('name') != None:
					key = input.get('name')
					value = input.get('value')
					if key != 'method_premium':
						if not payload.has_key(key):
							payload[key] = [value]
						else:
							payload[key].append(value)
		else:
			for input in form.xpath('//input'):
				if input.get('name') != None:
					key = input.get('name')
					value = input.get('value')
					if key != 'method_premium':
						if not payload.has_key(key):
							payload[key] = [value]
						else:
							payload[key].append(value)

		if captchakey != None:
			try:
				payload[captchakey] = GetImgValue(url=captchaimg, HostPage=HostPage, UserAgent=UserAgent, cookies=captchacookies, split=split)
			except:
				payload[captchakey] = "Processing Issue"
		if addkey != None:
			payload.update(addkey)
		if removekey != None:
			for key in removekey:
				try:
					del payload[key]
				except KeyError:
					pass
		Log(payload)

		if wait != 0:
			#wait required
			time.sleep(wait)

		headers['Content-Type'] = 'application/x-www-form-urlencoded'
		headers['Origin'] = 'http://'+domain
		headers['Referer'] = HostPage

		formaction = form.xpath('//'+elm+'form')[wform].get('action')
		if formaction != None and formaction != "":
			if formaction.split('/')[0] == 'http:':
				HostPage = formaction
			elif len(formaction.split('/')) == 2:
				HostPage = 'http://' + HostPage.split('/')[2] + formaction
			elif len(formaction.split('/')) == 1:
				HostPage = HostPage.rpartition('/')[0] + '/' + formaction

		r = session.post(HostPage, data=payload, headers=headers, allow_redirects=True)
		r.raise_for_status()
		r.cookies = session.cookies
		return r
	except:
		s.cookies = session.cookies
		return s


####################################################################################################
def SoftCaptcha(VideoPage):
	captchavalue1 = [chr(int(VideoPage.split("<span style='position:absolute;padding-left:")[1].split('#')[1].split(';')[0])), chr(int(VideoPage.split("<span style='position:absolute;padding-left:")[2].split('#')[1].split(';')[0])), chr(int(VideoPage.split("<span style='position:absolute;padding-left:")[3].split('#')[1].split(';')[0])), chr(int(VideoPage.split("<span style='position:absolute;padding-left:")[4].split('#')[1].split(';')[0]))] 
	px1 = [int(VideoPage.split("<span style='position:absolute;padding-left:")[1].split('px')[0]), int(VideoPage.split("<span style='position:absolute;padding-left:")[2].split('px')[0]), int(VideoPage.split("<span style='position:absolute;padding-left:")[3].split('px')[0]), int(VideoPage.split("<span style='position:absolute;padding-left:")[4].split('px')[0])]
	px2 = [int(VideoPage.split("<span style='position:absolute;padding-left:")[1].split('px')[0]), int(VideoPage.split("<span style='position:absolute;padding-left:")[2].split('px')[0]), int(VideoPage.split("<span style='position:absolute;padding-left:")[3].split('px')[0]), int(VideoPage.split("<span style='position:absolute;padding-left:")[4].split('px')[0])]
	px2.sort()
	captchavalue = ""
	i = 0
	k = 0
	while i < 4:
		while k < 4:
			if px2[i] == px1[k]:
				captchavalue = captchavalue + captchavalue1[k]
			k += 1
		k = 0
		i += 1
	Log("captchavalue: "+captchavalue)

	return captchavalue


####################################################################################################
def SolveMediaCaptcha(url, HostPage, Host, elm="", elm2="", wform=0, wScript=0, RecaptchaResponse=0, SessionCookies=None):

	if RecaptchaResponse == 0 or RecaptchaResponse == 1:
		headers = {'User-Agent': UserAgent, 'Referer': url}
		try:
			session1 = requests.session()
			if SessionCookies != None:
				session1.cookies = SessionCookies
			OpenUrl = session1.get(HostPage, headers=headers)
			VideoInfo = HTML.ElementFromString(OpenUrl.content).xpath('//noscript/iframe')[wScript].get('src')
			Log(VideoInfo)
			HostPageHTML = re.sub("\r\n\t", "", String.Quote(OpenUrl.content, usePlus=True))
			cookies = CookieDict(cookies=session1.cookies)

			session = requests.session()
			headers['Referer'] = HostPage
			req = session.get(VideoInfo, headers=headers)
			captchacookies = CookieDict(cookies=session.cookies)
			VideoSRC = HTML.ElementFromString(req.content).xpath('//div[@id="adcopy-outer"]/table/tr')
			try:
				VideoID = VideoSRC[0].xpath('./td/img')[0].get('src')
			except:
				VideoID = VideoSRC[0].xpath('./td/div/iframe')[0].get('src')
			adcopy_challenge = VideoID.split('=')[1]
			captchaimg = "http://api.solvemedia.com" + VideoID
		except:
			adcopy_challenge = ""
			HostPageHTML = ""
			captchaimg = "http://googlechromesupportnow.com/wp-content/uploads/2012/06/Installation-103-error-in-Chrome.png"

	if RecaptchaResponse == 0:
		VideoPage = SecondButtonPress(url=url, HostPage=HostPage, page=OpenUrl, elm=elm, elm2=elm2, wform=wform, cookies=cookies, addkey={"adcopy_challenge": adcopy_challenge, "referer": url}, captchakey="adcopy_response", captchaimg=captchaimg, captchacookies=captchacookies, split='TOP')
	elif RecaptchaResponse == 1:
		hosts = LoadData(fp=CAPTCHA_DATA)

		i = 1
		for gethost in hosts:
			if gethost[i]['host'] == Host:
				gethost[i]['url'] = url
				gethost[i]['HostPage'] = HostPage
				gethost[i]['page'] = HostPageHTML
				gethost[i]['adcopy_challenge'] = adcopy_challenge
				gethost[i]['UserAgent'] = UserAgent
				gethost[i]['captchacookies'] = captchacookies
				gethost[i]['thumb'] = captchaimg
				gethost[i]['cookies'] = cookies
				break
			else:
				i += 1

		JsonWrite(fp=CAPTCHA_DATA, jsondata=hosts)

		return True
	elif RecaptchaResponse == 2:
		hosts = LoadData(fp=CAPTCHA_DATA)
		Host = Host.replace("_2", "")

		i = 1
		for gethost in hosts:
			if gethost[i]['host'] == Host:
				RecaptchaResponse = gethost[i]['response']
				adcopy_challenge = gethost[i]['adcopy_challenge']
				VideoInfo = gethost[i]['page']
				VideoInfo = String.Unquote(VideoInfo, usePlus=True)
				GetUserAgent = gethost[i]['UserAgent']
				cookies = gethost[i]['cookies']
				break
			else:
				i += 1

		VideoPage = SecondButtonPress(url=url, HostPage=HostPage, page=VideoInfo, elm=elm, elm2=elm2, wform=wform, cookies=cookies, addkey={"adcopy_challenge": adcopy_challenge, "adcopy_response": RecaptchaResponse, "referer": url}, GetUserAgent=GetUserAgent)

	return VideoPage


####################################################################################################
def GoogleCaptcha(url, HostPage, Host, VideoInfo=None, RecaptchaResponse=0, cookies={}):

	if RecaptchaResponse == 0 or RecaptchaResponse == 1:
		savecookies = CookieDict(cookies=cookies)
		try:
			GoogleImgLink = "http://www.google.com/recaptcha/api/image?c="
			Googleurl = VideoInfo.split('<div id="recaptcha_widget"')[1].split('<script type="text/javascript" src="')[1].split(' ">')[0]
			headers = {'User-Agent': UserAgent}
			VideoID = requests.get(Googleurl, headers=headers)
			GoogleKey = VideoID.content.split("challenge : '")[1].split("'")[0]
			captchaimg = GoogleImgLink + GoogleKey
			HostPageHTML = re.sub("\r\n\t", "", String.Quote(VideoInfo, usePlus=True))
		except:
			GoogleKey = ""
			HostPageHTML = ""
			captchaimg = "http://googlechromesupportnow.com/wp-content/uploads/2012/06/Installation-103-error-in-Chrome.png"

	if RecaptchaResponse == 0:
		VideoPage = SecondButtonPress(url=url, HostPage=HostPage, page=VideoInfo, cookies=savecookies, addkey={"recaptcha_challenge_field": GoogleKey, "referer": url, "down_direct": 1, "method_premium": ""}, captchakey="recaptcha_response_field", captchaimg=captchaimg, split='LR')

	elif RecaptchaResponse == 1:
		hosts = LoadData(fp=CAPTCHA_DATA)

		i = 1
		for gethost in hosts:
			if gethost[i]['host'] == Host:
				gethost[i]['url'] = url
				gethost[i]['HostPage'] = HostPage
				gethost[i]['page'] = HostPageHTML
				gethost[i]['recaptcha_challenge_field'] = GoogleKey
				gethost[i]['UserAgent'] = UserAgent
				gethost[i]['thumb'] = captchaimg
				gethost[i]['cookies'] = savecookies
				break
			else:
				i += 1

		JsonWrite(fp=CAPTCHA_DATA, jsondata=hosts)

		return True
	elif RecaptchaResponse == 2:
		hosts = LoadData(fp=CAPTCHA_DATA)
		Host = Host.replace("_2", "")

		i = 1
		for gethost in hosts:
			if gethost[i]['host'] == Host:
				RecaptchaResponse = gethost[i]['response']
				VideoInfo = gethost[i]['page']
				VideoInfo = String.Unquote(VideoInfo, usePlus=True)
				GoogleKey = gethost[i]['recaptcha_challenge_field']
				GetUserAgent = gethost[i]['UserAgent']
				cookies = gethost[i]['cookies']
				break
			else:
				i += 1

		VideoPage = SecondButtonPress(url=url, HostPage=HostPage, page=VideoInfo, cookies=cookies, addkey={"recaptcha_challenge_field": GoogleKey, "recaptcha_response_field": RecaptchaResponse, "referer": url, "down_direct": 1, "method_premium": ""}, GetUserAgent=GetUserAgent)
		
	return VideoPage


####################################################################################################
def IncapsulaScript(DeString):
	b = DeString.split('b="')[1].split('"')[0]
	z = ""

	for i in xrange(0, len(b)-1, 2):
		z = z + chr(int(b[i:i+2], 16))
	URL = "http://billionuploads.com" + z.split('"GET","')[1].split('"')[0]

	return URL


####################################################################################################
def CookieDict(cookies):
	savecookies = {}
	for key, value in cookies.items():
		savecookies[key] = value

	return savecookies


####################################################################################################
def ErrorMessage(Host, LogError=0, InputError="", ErrorType=""):

	if LogError == 1:
		InputError = "Failed!  Host has changed code base of site!"
	elif LogError == 2:
		InputError = "Form Process issue -- Returns you to same page"
	elif LogError == 3:
		InputError = "Site is currently offline"
	elif LogError == 4:
		InputError = "Disabled do to recaptcha text enter"
	elif LogError == 5:
		InputError = "Disabled do to Chunked MP4"
	elif LogError == 6:
		InputError = "May Not work do to country restrictions"
	elif LogError == 7:
		InputError = "Not in list!!!"
	elif LogError == 8:
		InputError = "HTTP Steaming f4m not supported"
	elif LogError == 9:
		InputError = "Incorrect IP. Please refresh!!"

	Log(Host+" -- " + InputError)

	return ErrorVideo(ErrorType=ErrorType)


####################################################################################################
def ErrorVideo(ErrorType):

	if VideoError == "Enabled":
		if ErrorType == "":
			VideoMessage = R("Host_Down.mp4")
			#VideoMessage = "http://d3macfshcnzosd.cloudfront.net/010871413_main_l.mp4"
		elif ErrorType == "HostDown":
			VideoMessage = R("Host_Down.mp4")
		elif ErrorType == "VideoRemoved":
			VideoMessage = R("Video_Removed.mp4")
		elif ErrorType == "WrongIP":
			VideoMessage = R("Wrong_IP.mp4")
		elif ErrorType == "WrongCaptcha":
			VideoMessage = R("Wrong_Captcha.mp4")
		elif ErrorType == "UploadError":
			VideoMessage = R("Video_Removed.mp4")
		elif ErrorType == "GeolocationLockout":
			VideoMessage = R("Geolocation_Lockout.mp4")
	else:
		VideoMessage = "Error: Problem with getting Video File to play!"

	return VideoMessage


####################################################################################################
def GetHostPageURL(Host=None, url=None, HostPageInfo=None):

	if Host != None:
		session = requests.session()
		headers = {'User-Agent': UserAgent}
		req = session.get(url, headers=headers)
		HostPageInfo = HTML.ElementFromString(req.content)

	CURRENT_MOVIE2K_URL = url.split('/')[2]

	HostPageElm = HostPageInfo.xpath('//div[@id="maincontent5"]/div')[0]
	try:
		try:
			if CURRENT_MOVIE2K_URL == "www.movie2k.sx":
				GetDiv = HostPageElm.xpath('./div')[3]
				HostPage = GetDiv.xpath('./iframe')[0].get('src')
			else:
				HostPage = HostPageElm.xpath('./iframe')[0].get('src')
			LinkType = 1
		except:
			HostPage = HostPageElm.xpath('./embed')[0].get('src')
			LinkType = 2
	except:
		try:
			try:
				HostPage = HostPageInfo.xpath('//div[@id="emptydiv"]//script')[0].get('src')
				LinkType = 3	
			except:
				if CURRENT_MOVIE2K_URL == "www.movie2k.sx":
					GetDiv = HostPageElm.xpath('./div')[3]
					HostPage = GetDiv.xpath('./a')[0].get('href')
				else:
					try:
						HostPage = HostPageElm.xpath('./a')[0].get('href')
					except:
						HostPage = HostPageElm.xpath('./div[@id="emptydiv"]/a')[0].get('href')
				LinkType = 4
		except:
			try:
				HostPage = HostPageElm.xpath('./object/param')[0].get('value')
				LinkType = 5
			except:
				HostPage = None
				LinkType = 0

	return (HostPage, LinkType)