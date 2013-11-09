#Movie2k Plugin Introduction:

This is a Plex channel plugin that pulls in Movie and TV Episodes from the website Movie2k.to now moved to Movie4k.to.

![dashboard-thumbnail]

## Feedback Needed

[Forum Link][plexforum]
I would like some feedback on this plugin. Currently, friends and family have been using it.

#MOVIE2K CHANNEL INSTRUCTIONS:
##MOVIE2K PREFERENCES:


##Version:

Version is just that it's the current version of the Movie2k Plugin.

##Video Resolution:

Video Resolution has three choices:  480, 720 and 1080.  This will allow you set your resolution according to the device you want to playback on.

##Site URL:

Site URL allows you to choose the URL you want to pull your Movie and TV Shows from.  If you change from the default Site URL may require Plex Media Server to be restarted. Proxy servers can be used if the www.movie4k.to site URL is being blocked.  This has no effect on Host site URLs only MOVIE4k.  Only proxy effects on Host sites will be using the Tor setup.

Currently there are eleven URLs in the list: 
     Main Site for Movie4k: www.movie4k.to and it's IP address
     Proxy sites for Movie4k: www.movie.to, movie4k.co.in, movie4k.to.come.in, www.movie4kunblocked.co, www.movie2kproxy.org and
                                     www.movie2kproxy.com
     Main Site for Movie2k.tv: www.movie2k.tv and it's IP address
     Main Site for Movie2k.tl (German Content Only): www.movie2k.tl

##Number of Hosts Per Page:

Allows you to change the number of Hosts per page to be displayed.  Default is 5 per page.

##Use Description as Title:

For devices like the Apple TV PlexConnect that only display the title for an item with no summary discription underneath.  This will enable you to tell what hosts are on the next page and information about the host once selected.

##Play Error Video:

Play Error Video is to play error video instead of the the default ERROR screen when a video file can't be played.

##Top Pages Displayed:

Top Pages Displayed is to override and show the TOP Movies, TV Shows and Adult that are currently hidden and not updated on Movie4k.to and Movie2k.tv.  These sections do appear automatically when you select the Site URL www.movie2k.tl because the pages are maintained on that site.

##Adult Content:

Adult Content is to show the adult movies that are on Movie4k.to and Movie2k.tv.  By default this section is disabled and has to be enabled to view the content.  However, Movie2k.tl will not show any adult content reguardless because this site
does not have adult content enabled.

##Parental Lock:

Parental Lock is for password protecting the Adult Cotent section if it's enabled.

##Preferred Language:

Preferred Language allows you to filter and display only the language selected or if ALL is selected all languages are displayed.

##Username and Password Fields:

Username and Password for My Movie4k login and this allows you to get your messages and see your current uploads.  If the uploads are accepted you can watch them.  Make sure if you create accounts on Movie4k.to, Movie2k.tv and Movie2k.tl all three sites use the same username and password.

##Connect to Tor Network:

Connect to Tor Network allows you to use the Tor network via socks5 connection if enabled.

To use Tor proxy you will have to download and install Tor on your Plex Media Server machine (Should work for fine Windows, OSX, Linux).

To get the Plex transcoder to use Tor proxy server on Windows use an app like Proxifier it forces all net traffic to Tor when set up.  For OSX and Linux not real sure at the moment for a redirect method for Plex transcoder to Tor
proxy.

[Tor Link:][torlink] https://www.torproject.org/download/download-easy.html
[Proxifier Link:][proxifierlink] http://www.proxifier.com/

Make sure you have Tor Proxy server running before you try to use the plugin if it's enabled.

##Get New Tor IP Address:

Get New Tor IP Address  allows you to get a new Tor network IP address everytime you launch the Movie2k plugin if enabled.  This will require the following to get it to work you will need to put in a password and enable Generate Tor Hashed Password.  You will need to next look in your com.plexapp.plugins.movie2k.log file to get your hashed password, copy and past it into the torrc file found in the Tor Browser folder \Data\Tor...  Just past it at the bottom of the file.  You will see a log statement with - Example:
HashedControlPassword 16:C66BF3B72C28938B607CE71CC9949A2AF2AE579A0A54A8182439BFD982

##Generate Tor Hashed Password:

Generate Tor Hashed Password allows you to generate the HashedControlPassword from the Tor Control Password.

##Tor Control Password:

Tor Control Password is a password field used in generating the HashedControlPassword.  A password must be entered for the HashedControlPassword to be generated.

##Debug Options:

Debug Options are for testing Host sites.  When enabled the Plugin will only playback content from the Host site being debugged.  The following fields will be used with this.  You will need to fill in the Debug Host name along with either the Debug Host URL or Debug Movie2k URL.  This will allow you to see what errors are thrown in the Movie2k plugin log file if a Host site has changed their code structure.

##Debug Host Name:

Debug Host Name you will need to enter the enter the domain name with out the .com, .net, .tv, ect...  Example: www.flashx.tv and you would enter Flashx with the first letter in upper case.

##Debug Host URL:

Debug Host URL is the full path to the video from the Host you want to test.

##Debug Movie2k URL:

Debug Movie2k URL is the full path to the Host on the Movie4k.to, Movie2k.tv or Movie2k.tl

##Other Movie2k Plugin Info:

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

##Resolved Issues:

1.  It now loads up on Plex Media Server running on Mac OSX v10.6.8.

2.  Now MOVIE2K plugin will work with the iOS.

3.  With the latest version of Plex Media Server.  Plexconnect now works with Apple TV with this RTMP channel.

[dashboard-thumbnail]: https://raw.github.com/Joecowboy/MOVIE2K.bundle/master/Contents/Resources/icon-default.png
[plexforum]: http://forums.plexapp.com/index.php/topic/75524-new-channel-movie2k-plugin-for-movie4kto-website/
[torlink]: https://www.torproject.org/download/download-easy.html
[proxifierlink]: http://www.proxifier.com/