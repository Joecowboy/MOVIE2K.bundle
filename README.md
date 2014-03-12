#Movie2k Plugin Introduction:

This is a Plex channel plugin that pulls in Movie and TV Episodes from the website Movie2k.to now moved to Movie4k.to, Movie2k.tv, Movie2k.sx and Movie2k.tl.  All the sites have a little bit different content with different Host line ups for the movies and tv shows.

![dashboard-thumbnail]

###Feedback Needed

[Forum Link][plexforum] - I would like some feedback on this plugin. Currently, friends and family have been using it.

#MOVIE2K CHANNEL INSTRUCTIONS:
##MOVIE2K PREFERENCES:


###Version:

Version is just that it's the current version of the Movie2k Plugin.

###Video Resolution:

Video Resolution has three choices:  480, 720 and 1080.  This will allow you set your resolution according to the device you want to playback on.

###Site URL:

Site URL allows you to choose the Proxy URL or IP address you want to pull your Movie and TV Shows from.  If you change the Site URL may require Plex Media Server to be restarted. Proxy servers can be used if the www.movie4k.to site URL is being blocked.  This has no effect on Host site URLs only MOVIE4k.  Only proxy effects on Host sites will be using the Tor setup.

Currently there are eleven URLs in the list:

-**Main Site for Movie4k:** IP address

-**Proxy sites for Movie4k:** www.movie.to, movie4k.co.in, movie4k.to.come.in, www.movie4kunblocked.co, www.movie2kproxy.org and www.movie2kproxy.com

-**Main Site for Movie2k.tv:** IP address

###Plex/Web Search Site URL:

Plex/Web Search Site URL allows you to choose the URL you want Plex/Web to search your Movie and TV Shows from. This has no effect on the search feature displayed on other client devices such as the Roku.  All the Main sites have a little bit different content with different Host line ups for the movies and tv shows. If you change from the default Site URL may require Plex Media Server to be restarted. Proxy servers can be used if the www.movie4k.to site URL is being blocked.  This has no effect on Host site URLs only MOVIE4k.  Only proxy effects on Host sites will be using the Tor setup.

Currently there are eleven URLs in the list:

-**Main Site for Movie4k:** IP address

-**Proxy sites for Movie4k:** www.movie.to, movie4k.co.in, movie4k.to.come.in, www.movie4kunblocked.co, www.movie2kproxy.org and www.movie2kproxy.com

-**Main Site for Movie2k.tv:** IP address

###Number of Hosts Per Page:

Allows you to change the number of Hosts per page to be displayed.  Default is 1 per page.

###Autoresume Downloads:

This is so you can disable and enable autoresume of downloads you have in your Watchit Later lineup.  It will check every 5 minutes for a failed download and try to autoresume the download.  This is so you can have more control if you don't want to poll for downloads while watching a show.

###Manual Resume Downloads:

What this does if you go to Watchit Later videos and a video download has failed it will try force the download where it left off.  If an error message displays other than video removed or host down you can try back later to see if autoresume was able to trigger the download or manually trigger it yourself.  If it's downloading it will display the status of the download.

###Autopatch Runtime.py:

What this does is update the runtime.py and docutils.py files so Watchit Later will play your downloaded videos.  You will need to leave it enabled to continually update the files since Plex Media Server will write over them once a hour.  You do not need to restart the Plex Media Server with the auto patcher it resets the Cor Services in the background on update.

###FLV Download Skip:

If enabled it will prompt you if you are trying to download an FLV file from a Host site and tell you to choose another Host.  Also, supports selecting MP4, AVI or MKV for download only.

###Play Error Video:

Play Error Video is to play error video instead of the the default ERROR screen when a video file can't be played.

###Top Pages Displayed:

Top Pages Displayed is to override and show the TOP Movies, TV Shows and Adult that are currently hidden and not updated on Movie4k.to and Movie2k.tv.  These sections do appear automatically when you select the Site URL www.movie2k.tl because the pages are maintained on that site.

###Adult Content:

Adult Content is to show the adult movies that are on Movie4k.to and Movie2k.tv.  By default this section is disabled and has to be enabled to view the content.  However, Movie2k.tl will not show any adult content reguardless because this site
does not have adult content enabled.

###Parental Lock:

Parental Lock is for password protecting the Adult Cotent section if it's enabled.

###Preferred Language:

Preferred Language allows you to filter and display only the language selected or if ALL is selected all languages are displayed.

###Username and Password Fields:

Username and Password for My Movie4k login and this allows you to get your messages and see your current uploads.  If the uploads are accepted you can watch them.  Make sure if you create accounts on Movie4k.to, Movie2k.tv and Movie2k.tl all three sites use the same username and password.

###RealDebrid Username, Password and Email Pin Fields:

This allows you to log into and use your RealDebrid account if you have one to access the premium video streams if the Host site you select is in their Host list.   The Email Pin field is if you use Tor network or your IP address changes a lot they may require you to log into your email account associated with your RealDebrid account and get a pin number to access their site.

###Connect to Tor Network:

Connect to Tor Network allows you to use the Tor network via socks5 connection if enabled.

To use Tor proxy you will have to download and install Tor on your Plex Media Server machine (Should work for fine Windows, OSX, Linux).

To get the Plex transcoder to use Tor proxy server on Windows and Mac OSX use an app like Proxifier it forces all net traffic to Tor when set up.  For Linux not real sure at the moment for a redirect method for Plex transcoder to Tor proxy.

-[Tor Link:][torlink] https://www.torproject.org/download/download-easy.html
-[Proxifier Link:][proxifierlink] http://www.proxifier.com/

Make sure you have Tor Proxy server running before you try to use the plugin if it's enabled.

OK UPDATE YOU NEED TO GET Vidalia they ripped it out of the 3.5 tor package:  So gives you no control over who you connect to. NOT GOOD!!!!!
-[Vadilia Link:][vidalialink] https://people.torproject.org/~erinn/vidalia-standalone-bundles/

Make sure you have Tor Proxy server running before you try to use the plugin if it's enabled.

Setting up Proxifier select from the menu Profile and then Proxy Servers.  Click the Add button, for the IP address put in 127.0.0.1 port 9150 type is SOCKS5

Heres a Tutorial: How to change the IP address in TOR to a specific country’s IP
-[Change IP Link:][changeiplink] http://www.bloomgeek.com/featured/how-to-change-the-ip-address-in-tor-to-a-specific-countrys-ip

###Get New Tor IP Address:

Get New Tor IP Address  allows you to get a new Tor network IP address everytime you launch the Movie2k plugin if enabled.  This will require the following to get it to work you will need to put in a password and enable Generate Tor Hashed Password.  You will need to next look in your com.plexapp.plugins.movie2k.log file to get your hashed password, copy and past it into the torrc file found in the Tor Browser folder \Data\Tor...  Just past it at the bottom of the file.  You will see a log statement with - Example:
HashedControlPassword 16:C66BF3B72C28938B607CE71CC9949A2AF2AE579A0A54A8182439BFD982

###Generate Tor Hashed Password:

Generate Tor Hashed Password allows you to generate the HashedControlPassword from the Tor Control Password.

###Tor Control Password:

Tor Control Password is a password field used in generating the HashedControlPassword.  A password must be entered for the HashedControlPassword to be generated.

###Debug Options:

Debug Options are for testing Host sites.  When enabled the Plugin will only playback content from the Host site being debugged.  The following fields will be used with this.  You will need to fill in the Debug Host name along with either the Debug Host URL or Debug Movie2k URL.  This will allow you to see what errors are thrown in the Movie2k plugin log file if a Host site has changed their code structure.

###Link Type:

Link Type is allows you to choose they type of link you want to test.  They are 1 - Iframe, 2 - Embeded, 3 - Script and 4 - Anchor links.

###Debug Host Name:

Debug Host Name you will need to enter the enter the domain name with out the .com, .net, .tv, ect...  Example: www.flashx.tv and you would enter Flashx with the first letter in upper case.

###Debug Host URL:

Debug Host URL is the full path to the video from the Host you want to test.

###Debug Movie2k URL:

Debug Movie2k URL is the full path to the Host on the Movie4k.to, Movie2k.tv or Movie2k.tl

###Other Movie2k Plugin Info:

Sometimes the plugin might error and this could be do to a timeout error trying to load the content.  Try to load it again and it might take a few tries depending on the internet connection.  Also, it might take a little time to load the content so be patient and allow the content to load.

The Trailer Addict search does not show up in Plex Web do to the way search is handled but works fine on the Roku.  Only search function in Plex Web is Movie4k.  The Expermental Transcoder does work for Trailer Addict on the Roku.  

To enter My Favorite Movie4k URL, Parental Lock password or Captcha text, Roku users must be using version 2.6.6 or later of the Plex Roku Channel (currently the PlexTest channel)  You can use the Roku online remote control to enter your Movie4k URLs.  It can be found here: http://www.remoku.tv/

##CURRENT ISSUES:

1. Google nor SolveMedia Captcha responce are not being processed correctly by the Host websites.  After the form is posted the site returns you to the same page.

2. SolveMedia Captcha image might not show up all the time.  Need feed back and or ideas to why this could be happening.

3. Need a way to redirect the transcoder for OS X and Linux to the Tor network same way Proxifier does when it's set up to use Tor network.  Because nearly all the sebsites check the IP address for the video that is being played and so if it does not match will not stream.

4. Not sure if it's an issue or not but need a way to launch these apps before the transcoder kicks up to redirect transcoder traffic to Tor network.

5. Need to add OCR for OS X and Linux.  Eventhough, OCR works about 1% of the time.  Might as well add it.

6. Need to add OS check for these last two items.

7. For timeout issues with Apple TV and Plex/Web go to the Movie2k Plugin Preferences change Number of Hosts Per Page from the default of 5 to 1.

##Resolved Issues:

1.  It now loads up on Plex Media Server running on Mac OSX v10.6.8.

2.  Now MOVIE2K plugin will work with the iOS.

3.  With the latest version of Plex Media Server.  Plexconnect now works with Apple TV with this RTMP channel and you can also search.  Also, for timeout issues in Movie2k Plugin Preferences change Number of Hosts Per Page from the default of 5 to 1.  You currently cannot set preferences in any of the Channel plugins on Plexconnect. That input functionality has not been added. You have to do all that on another client/device.

4. LG TV needs the file Info.plist edited found in MOVIE2k.bundle/content folder (This will impact the RTMP Host sites):
	<key>PlexFrameworkFlags</key>
	<array>
		<string>UseRealRTMP</string>
	</array>

  Changed to:
	<key>PlexFrameworkFlags</key>
	<array>
		<string>*</string>
	</array>

[dashboard-thumbnail]: https://raw.github.com/Joecowboy/MOVIE2K.bundle/master/Contents/Resources/icon-default.png
[plexforum]: http://forums.plexapp.com/index.php/topic/75524-new-channel-movie2k-plugin-for-movie4kto-website/
[torlink]: https://www.torproject.org/download/download-easy.html
[proxifierlink]: http://www.proxifier.com/
[vidalialink]: https://people.torproject.org/~erinn/vidalia-standalone-bundles/
[changeiplink]: http://www.bloomgeek.com/featured/how-to-change-the-ip-address-in-tor-to-a-specific-countrys-ip