import os
import shutil
import time
import astral
import astropy.units as u
from astroplan import Observer
from astropy.time import Time
from astropy.coordinates import EarthLocation


path = "C:/Users/Mike/Documents/Temp/" # Data directory to remove data from

latitude = 43.19301
longitude = -81.31555
elevation = 327
site = "Elginfield"

# Calculate hours of darkness
location = EarthLocation.from_geodetic(longitude*u.deg, latitude*u.deg, elevation*u.m)
obs = Observer(location=location, name=site)
now = time.time() # Current time in seconds
apo = Observer.at_site("APO")
time = Time(now, format='unix')

sunrise = apo.sun_set_time(time, which='nearest', horizon=-12*u.deg)
sunset = apo.sun_rise_time(time, which='nearest', horizon=-12*u.deg)

darkness = abs((sunrise-sunset)*24).value

# Calculate minimum amount of space needed
minsize = darkness*40*60*60*(2048*2048*1.5*2+246)/1000000000000

print("For the %.2f hours of darkness tonight, we need %.2f TB of space.\n" % (darkness, minsize))

# Max age (in seconds) of directories to keep
maxdays = 86400*1 

# Check disk space
total, used, free = shutil.disk_usage(path)
print("***Disk Summary ***")
print("Totes McGroats: %.3f TB" % (total // (2**30) / 1000))
print("Used Space: %.3f TB" % (used // (2**30) / 1000))
print("Free Space: %.3f TB\n" % (free // (2**30) / 1000))

print("We need a minimum of %d TB free\n" % minsize)

if (free // (2**30) / 1000) < minsize:
	print("We need to clean up!")
	for root, directories, files in os.walk(path):
		for dir in directories:
			
			timestamp = os.path.getmtime(os.path.join(root, dir))

			if (now - maxdays) > timestamp:
				try:
					print("Removing directory ", os.path.join(root,dir))
					shutil.rmtree(os.path.join(root,dir))
				except Exception as e:
					print(e)

			# Check free space and exit loop if we have enough for the night
			total, used, free = shutil.disk_usage(path)
			if free > minsize:
				break