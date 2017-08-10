#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# čžřě+áýčíáý+í

"""
name: Instagram-downloader -- Downloader for Instagram photos in full resolution 
autor: Černý Jan
email: cerny.jan@hotmail.com
version: 0.5
license: viz. LICENSE
"""

from builder import Builder
from worker import Worker

import platform
import ctypes
from time import sleep
import urllib2
import json
from sys import exit
import os.path
import timeit
from sys import argv


def test_connection():
	"""
	Checking the functional connection to the Internet
	query 'https://www.instagram.com'
	if unsuccessful - retries after 10s
	"""
	loop = True
	cycle = 2
	while loop:
		try:
			con = urllib2.urlopen("https://www.instagram.com")
			con.read()
			loop = False
			if debug:
				print "internet connection OK"
			return True
		except IOError:
			if debug:
				print "failed connection of internet"
				print "repeat attempt\n"
			if cycle > 0:
				cycle -= 1
				sleep(10)
			else:
				return False


def account_exists(user):
	url = "https://www.instagram.com/" + user 
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	try:
		f = opener.open(req)
	except urllib2.HTTPError, err:
		if err.code == 404:
			return False
		else:
			raise
	return True


def main():
	global debug
	if (len(argv) == 2) and argv[1] == "--debug":
		debug = True
	else:
		debug = False
	
	print "\r"
	print "******************************************************************"
	print "Instagram downloader v0.5 \t author: Černý Jan \t 2016-2017"
	print "******************************************************************"
	
	user = raw_input('user account: ').strip()

	#internet connection test
	if test_connection():
		pass
	else:
		exit("app down")

	#account exists test
	if account_exists(user):
		pass
	else:
		exit("Account does not exist")

	url = "https://www.instagram.com/" + user + "/media/"
	
	start_time = timeit.default_timer()

	ib = Builder(user, debug)
	ib.set_images()

	if debug:
		print "found " + str(ib.get_number_of_images()) + " photo(s)"
	
	w = Worker(ib.get_images(), user, debug)
	w.work()

	elapsed = round((timeit.default_timer() - start_time), 2)

	path = user
	print "\nTotal: " + str(len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])) + " photo(s) " + "in " + str(elapsed) + " seconds"
	exit("--successfully finished--")

			
if __name__ == '__main__':
	debug = False
	#changing the name of a running process for a better overview of the means utilized
	if platform.system() == "Linux":
		LIBC = ctypes.CDLL('libc.so.6')
		PROC_NAME = "000-Instagram-downloader"
		LIBC.prctl(15, '%s\0' %PROC_NAME, 0, 0, 0)
		#a delay of 1s
		sleep(1)
	
	#main thread
	main()
