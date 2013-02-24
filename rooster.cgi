#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Made by Stefan Patelski

# enable debugging
import cgitb
import cgi
import sys
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

import urllib2
from BeautifulSoup import BeautifulSoup # non-standard library
from icalendar import Calendar, Event, UTC, vText # non-standard library
from datetime import datetime, date, timedelta, time
import random
from dateutil import zoneinfo # non-standard library


#print for testing purposes:
def testprint():
	for array in datamatrix:
		for element in array:
			print element
		print "__________________________________________"

#response = urllib2.urlopen('https://venus.tue.nl/owinfo-cgi/owi_0695c.opl?vakcode=0A531&studiejaar=2011&language=&printfriendly=Y')
#html = response.read()
#soup = BeautifulSoup(html)
#print soup.html.body.div.nextSibling.nextSibling.div.div

def addCourse(vakcode,studiejaar):
	#retrieve raw html from owinfo and select the stuff we need:
	response = urllib2.urlopen('https://venus.tue.nl/owinfo-cgi/owi_0695c.opl?vakcode='+vakcode+'&studiejaar='+studiejaar+'&language=&printfriendly=Y')
	html = response.read()
	soup = BeautifulSoup(html)
	data = soup.html.body.div.nextSibling.nextSibling.div.div.findAll('td', valign="top")
	course = soup.find('th', align="left").string

	#retrieve the useful strings from the beautifulSoup data and put them in a nicely ordered matrix:
	datamatrix = [[]]
	i = 0
	for element in data:
		if len(datamatrix[i])<8:
			if len(datamatrix[i])==5:
				datamatrix[i].append(element.a.string)
			else:
				datamatrix[i].append(element.renderContents())
		else:
			datamatrix.append([])
			i=i+1
			if len(datamatrix[i])==5:
				datamatrix[i].append(element.a.string)
			else:
				datamatrix[i].append(element.renderContents())
	
	if len(datamatrix[0])>3:
		for array in datamatrix:
			array.append(course)
		return datamatrix
	else:
		return []

datamatrix = []

def getCourses(vakcodes,jaar):
	datamatrix = []
	for vak in vakcodes:
		datamatrix = datamatrix+addCourse(vak,jaar)
	return datamatrix

#datamatrix = getCourses(["0A531","0I003","0A631","2ID05","2II07","0A536","2IC05","0A632"],"2011")
parameters = cgi.FieldStorage()
vcstring = parameters["vakcodes"].value
vclist = vcstring.split(",")
jaargang = parameters["jaargang"].value
datamatrix = getCourses(vclist,jaargang)

for array in datamatrix:
	#transform the html string of start/end dates into an array of python datetime objects for each day the event occurs:
	startdate = date(int(array[3][6]+array[3][7]+array[3][8]+array[3][9]),int(array[3][3]+array[3][4]),int(array[3][0]+array[3][1]))
	enddate = date(int(array[3][22]+array[3][23]+array[3][24]+array[3][25]),int(array[3][19]+array[3][20]),int(array[3][16]+array[3][17]))
	dates = []
	curdate = startdate
	oneweek = timedelta(weeks=1)
	while curdate <= enddate:
		dates.append(curdate)
		curdate = curdate + oneweek
	array.append(dates)
	#transform hour to start/end times:
	if array[2] == "1":
		starttime = time(8,45)
		endtime = time (9,30)
	elif array[2] == "2":
		starttime = time(9,45)
		endtime = time (10,30)
	elif array[2] == "3":
		starttime = time(10,45)
		endtime = time (11,30)
	elif array[2] == "4":
		starttime = time(11,45)
		endtime = time (12,30)
	elif array[2] == "5":
		starttime = time(13,45)
		endtime = time (14,30)
	elif array[2] == "6":
		starttime = time(14,45)
		endtime = time (15,30)
	elif array[2] == "7":
		starttime = time(15,45)
		endtime = time (16,30)
	elif array[2] == "8":
		starttime = time(16,45)
		endtime = time (17,30)
	elif array[2] == "9":
		starttime = time(18,45)
		endtime = time (19,30)
	elif array[2] == "10":
		starttime = time(19,45)
		endtime = time (20,30)
	elif array[2] == "11":
		starttime = time(20,45)
		endtime = time (21,30)
	else:
		starttime = time(21,45)
		endtime = time (22,30)
	array.append(starttime)
	array.append(endtime)

timezone = zoneinfo.gettz("Europe/Amsterdam")
cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')
for array in datamatrix:
	for element in array[9]:
		event = Event()
		event.add('summary', array[8])
		event.add('description', array[6] + " -- " + array[7])
		#event.add('description', array[6] + " -- opmerkingen: " + array[7] + " -- docent(en): " + array[4])
		event.add('dtstart', datetime(element.year,element.month,element.day,array[10].hour,array[10].minute,0,tzinfo=timezone))
		event.add('dtend', datetime(element.year,element.month,element.day,array[11].hour,array[11].minute,0,tzinfo=timezone))
		event.add('dtstamp', datetime(element.year,element.month,element.day,0,10,0,tzinfo=timezone))
		event['uid'] = str(element.year)+str(element.month)+str(element.day)+str(array[10].hour)+str(array[10].minute)+str(int(random.uniform(0,100000)))
		event['location'] = vText(array[5])
		event.add('priority', 5)
		cal.add_component(event)

#f = open('example.ics', 'wb')
#f.write(cal.as_string())
#f.close()

print cal.as_string()