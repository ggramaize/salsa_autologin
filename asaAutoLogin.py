#!/usr/bin/python
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup 
HTMLSoup = BeautifulSoup

import cmd
import time
import sys
import urllib
import urllib2

__loginURL = "https://webauth.telecom-bretagne.eu/login.html"
__checkURL = "https://webauth.telecom-bretagne.eu/logout.html"
__username = "someuser"
__password = "********"


# /// Polls to know if user is logged in
# Logged in: 1 ; logged out: 0
def pollServer(url):
	result = ""
	
	# Fetch page
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)

	hSoup = HTMLSoup( response.read() )
	inputs = hSoup.find("input", {"name": "userStatus"})
	result = inputs['value']
	
	return result
# /////////////////////////////////////

# ///// Static login request //////////
def sendLoginInformations(url, username, password):
	values = {'buttonClicked': '4', 
		  'err_flag': '0', 
		  'err_msg': '', 
		  'info_flag': '0',
		  'info_msg': '',
		  'redirect_url': '',
		  'username': username,
		  'password': password }
	
	headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux i686; rv:18.0) Gecko/20100101 Firefox/18.0 Iceweasel/18.0' }

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	he_page = response.read()

# /////////////////////////////////////

try:
	while 1:
		asaAuthState = pollServer( __checkURL )
		if asaAuthState == "0":
			sendLoginInformations( __loginURL, __username, __password)
			asaAuthState = pollServer( __checkURL )
			if asaAuthState == "0":
				print "Authentication failure. Check your credentials and try again."
				sys.exit(255)
			else:
				print "Login successful :)"
		else:
			print "Already authenticated, ignoring..."
		
		time.sleep(60)
except KeyboardInterrupt:
	print "Don't forget to log out if applicable, goodbye!"
	sys.exit(0)


	

