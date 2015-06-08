#!/usr/bin/env python
import sys
from os import listdir
from os.path import exists, isfile, join
from fnmatch import filter
from pexif import JpegFile

import time
import datetime
s = "01/12/2011"

usage = """Usage: gps-correct.py dirname"""
notexist = """path is not exist"""

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    http://stackoverflow.com/questions/4913349
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

if len(sys.argv) != 2:
	print >> sys.stderr, usage
	sys.exit(1)

mypath = sys.argv[1]
if exists(mypath) == False:
	print >> sys.stderr, notexist
	sys.exit(1)

files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
files =  filter(listdir(mypath), '*.[Jj][Pp][Gg]')
files = [ join(mypath,f) for f in files  ]
#print files

pLan = 0
pLat = 0
pTs = 0

for f in files:
	ef = JpegFile.fromFile(f)
	g = ef.get_geo()
	primary = ef.get_exif().get_primary()
	cTs = time.mktime(datetime.datetime.strptime(primary.DateTime, "%Y:%m:%d %H:%M:%S").timetuple())
	cLat = g[0]
	cLan = g[1]
	dist = haversine(pLan, pLat, cLan, cLat)
	dTs = cTs - pTs
	if pLan ==  0:
		print "%s, %lf, %lf" % (f, 0, 0)
	else:
		print "%s, %lf, %lf" % (f, dist, dTs)
	pLat = g[0]
	pLan = g[1]
	pTs = cTs
	#ef.dump()