#!/usr/bin/env python
# [PoC] tesseract OCR script - tuned for scr.im captcha
#
# Chris John Riley
# blog.c22.cc
# contact [AT] c22 [DOT] cc
# 12/10/2010
# Version: 1.0
#
# Changelog
# 0.1> Initial version taken from Andreas Riancho's \
#      example script (bonsai-sec.com)
# 1.0> Altered to use Python-tesseract, tuned image \
#      manipulation for scr.im specific captchas
#
#
# Perform OCR using tesseract-ocr library


# Setting up imports
import os, sys
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

from tesseract import image_to_string
from PIL import Image
from PIL import TiffImagePlugin
from PIL import ImageEnhance
import cStringIO
import hashlib
import time


####################################################################################################
def GetImgValue(url, HostPage, UserAgent, cookies, split=None):

	headers = {}
	headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	headers['Connection'] = 'keep-alive'
	headers['Host'] = url.split('/')[2]
	headers['Referer'] = HostPage
	headers['User-Agent'] = UserAgent

	imgData = requests.get(url, headers=headers, cookies=cookies).content
	im = cStringIO.StringIO(imgData)
	img = Image.open(im)
	img = img.convert("RGBA")

	pixdata = img.load()

	enh = ImageEnhance.Contrast(img)
	enh.enhance(1.3).show("30% more contrast")

	#  Make the letters bolder for easier recognition

	for y in xrange(img.size[1]):
		for x in xrange(img.size[0]):
			if pixdata[x, y][0] < 90:
				pixdata[x, y] = (0, 0, 0, 255)

	for y in xrange(img.size[1]):
		for x in xrange(img.size[0]):
			if pixdata[x, y][1] < 136:
				pixdata[x, y] = (0, 0, 0, 255)

	for y in xrange(img.size[1]):
		for x in xrange(img.size[0]):
			if pixdata[x, y][2] > 0:
				pixdata[x, y] = (255, 255, 255, 255)


	if split == 'LR' or split == 'TB':
		img1 = Crop(img=img, split=split, half=1)
		img2 = Crop(img=img, split=split, half=2)
		img1.save("input-black1.gif", "GIF")
		img2.save("input-black2.gif", "GIF")

		#  Make the image 1 bigger (needed for OCR)
		im_orig = Image.open('input-black1.gif')
		big1 = im_orig.resize((1000, 500), Image.NEAREST)

		ext = ".tif"
		big1.save("input-NEAREST1" + ext, "TIFF")
		image1 = Image.open('input-NEAREST1.tif')

		#  Make the image 2 bigger (needed for OCR)
		im_orig = Image.open('input-black2.gif')
		big2 = im_orig.resize((1000, 500), Image.NEAREST)

		ext = ".tif"
		big2.save("input-NEAREST2" + ext, "TIFF")
		image2 = Image.open('input-NEAREST2.tif')

		recaptcha1 = image_to_string(image1)
		recaptcha2 = image_to_string(image2)
		recaptcha = recaptcha1 + " " + recaptcha2
	else:
		if split == 'TOP':
			img = Crop(img=img, split=split)

		img.save("input-black.gif", "GIF")

		#  Make the image bigger (needed for OCR)
		im_orig = Image.open('input-black.gif')
		big = im_orig.resize((1000, 500), Image.NEAREST)

		ext = ".tif"
		big.save("input-NEAREST" + ext, "TIFF")
		image = Image.open('input-NEAREST.tif')

		recaptcha = image_to_string(image)

	return recaptcha


####################################################################################################
def Crop(img, split, half=0):

	#  get the image's width and height in pixels
	width, height = img.size

	if split == 'LR':
		if half == 1:
			left = 0
			upper = 0
			right = width/2
			lower = height
		elif half == 2:
			left = width/2 - 30
			upper = 0
			right = width
			lower = height
	if split == 'TB':
		if half == 1:
			left = 0
			upper = 0
			right = width
			lower = height/2
		elif half == 2:
			left = 0
			upper = height/2
			right = width
			lower = height
	if split == 'TOP':
		left = 0
		upper = 15
		right = width
		lower = height

	box = (left, upper, right, lower)
	area = img.crop(box)

	return area


####################################################################################################
def SplitImageLetters(img):
	letters = SeperateLetters(img=img)

	# New code is here. We just extract each image and save it to disk with
	# what is hopefully a unique name
  
	count = 0
	for letter in letters:
		m = hashlib.md5()
		im3 = img.crop(( letter[0] , 0, letter[1],img.size[1] ))
		m.update("%s%s"%(time.time(),count))
		im3.save("./%s.gif"%(m.hexdigest()))
		count += 1


####################################################################################################
def SeperateLetters(img):

	#  Separating letters:
	saut = 9
	inletter = False
	foundletter=False

	start_ab = 0
	end_ab = 0
	start_or = img.size[1]-1
	end_or = 0
	size = 0

	debut = True

	letters = []

	for y in range(0,img.size[0],saut): # slice across
		for x in range(0,img.size[1],1): # slice down
			pix = img.getpixel((y,x))
			if pix != 255:
				start_or = min(start_or,x)
				end_or = max(end_or,x)
				inletter = True

		if foundletter == False and inletter == True:
			foundletter = True
			start_ab = y

		if foundletter == True and inletter == False:
			foundletter = False
			end_ab = y
			size = max(size,end_ab)
			letters.append((start_ab,end_ab,start_or,end_or))
			start_or = img.size[1]-1
			end_or = 0
		inletter=False

	return letters