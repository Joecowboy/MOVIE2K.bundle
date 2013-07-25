####################################################################################################
# Setting up imports

import simplejson
import demjson
import urllib
import urllib2
import re
import os


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
		SystemData = LoadData(fp=fp, CaptchaData=CaptchaData, LoadFile=False)
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
	jsondata = jsondata + '{3 : {host: "Clicktoview", url: "", HostPage: "", page: "", recaptcha_challenge_field: "", response: "", UserAgent: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{4 : {host: "Vidbux", url: "",  HostPage: "", page: "", adcopy_challenge: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}},\n'
	jsondata = jsondata + '{5 : {host: "Vidxden", url: "",  HostPage: "", page: "", adcopy_challenge: "", response: "", UserAgent: "", cookies: "", captchacookies: "", thumb: ""}}\n'
	jsondata = jsondata + ']'
	
	JsonWrite(fp=fp, jsondata=jsondata)

	return jsondata


####################################################################################################
#The JSON file is saved in the data cache for this plugin setup by Plex
def JsonWrite(fp, jsondata):
	f = open(fp, "w+")
	f.write(str(jsondata).replace("u'", "'"))
	f.close()

	return True


#############################################################################################################################
# This function loads the json data file
def LoadData(fp, CaptchaData=None, LoadFile=True):
	if LoadFile:
		CaptchaData = JsonOpen(fp=fp)

	try:
		obj = simplejson.loads(CaptchaData)
	except:
		obj = demjson.decode(CaptchaData)

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
	DEBUG(script)
	try:
		parameters = script.split(";',")
		CKtable = int(parameters[1].split(',')[0])
	except:
		parameters = script.split("}',")
		CKtable = int(parameters[1].split(',')[0])

	k = parameters[1].split(",'")[1].split("'.")[0].split('|')
	c = int(parameters[1].split(',')[1])
	p = parameters[0].split('return p}')[1].replace("\\", "")

	#if CKtable == 23:
	#	table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m']
	#elif CKtable == 26:
	#	table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
	#elif CKtable == 34:
	#	table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x']
	if CKtable <= 36:
		table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','10','11','12','13','14','15','16','17','18','19','1a','1b','1c','1d','1e','1f','1g','1h','1i','1j','1k','1l','1m','1n','1o','1p','1q','1r','1s','1t','1u','1v','1w','1x','1y','1z','20','21','22','23','24','25','26','27','28','29','2a','2b','2c','2d','2e','2f','2g','2h','2i','2j','2k','2l','2m','2n','2o','2p','2q','2r','2s','2t','2u','2v','2w','2x','2y','2z','30','31','32','33','34','35','36','37','38','39','3a','3b','3c','3d','3e','3f','3g']
	#elif CKtable == 41:
	#	table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E']
	#elif CKtable == 46:
	#	table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J']
	elif CKtable <= 53:
		table = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q']
		
	while c >= 0:
		c = c - 1
		if k[c] != "":
			p = re.sub(r'\b'+table[c]+r'\b', k[c], p)
	DEBUG(p)
	try:
		try:
			try:
				try:
					p = p.split('name="src"value="')[1].split('"')[0]
				except:
					p = p.split('name="src" value="')[1].split('"')[0]
			except:
				p = p.split("file','")[1].split("'")[0]
		except:			
			try:
				p = p.split("file':'")[1].split("'")[0]
			except:
				p = p.split('file:"')[1].split('"')[0]
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
		
	DEBUG(p)
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
    DEBUG(temp5)
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