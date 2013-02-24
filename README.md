ScheduleScraper
===============

Scrapes the course schedule from the website of Eindhoven University of Technology and puts it in ical format.
It returns an ical file by navigating to "http://yourdomain.com/cgi-bin/rooster.cgi?jaargang=2012&vakcodes=2IN05,2IW65,2IS05".
Here, the parameter "jaargang" should contain the first part of the academic year, so e.g. "2012" for the academic year "2012/2013".
The parameter "vakcodes" should contain a comma-seperated list of all course codes that you want to schedule.
