####################################################################################################
# Set Up Tor Network Proxy
# This will be be used for Hosting sites that Block Countries - StreamCloud.eu & TheFile.me
# Or use it to hide your tracks...

import socket

# Import SocksiPy
import sockschain as socks
socks.DEBUG = Log

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
		if CheckHash != 'Disabled' and password != None:
			GenerateTorHashPassword(secret=password)
		if ChangeIP != 'Disabled' and password != None:
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