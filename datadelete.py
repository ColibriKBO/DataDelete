import os
import shutil
import time

path = "C:/Users/Mike/Documents/Temp/"

now = time.time()
maxdays = 86400*1 # max age of directories to keep

minsize = 10 # Min available space in TB before deleting files

total, used, free = shutil.disk_usage(path)
print("Total: %.3f TB" % (total // (2**30) / 1000))
print("Used: %.3f TB" % (used // (2**30) / 1000))
print("Free: %.3f TB" % (free // (2**30) / 1000))

print("We need a minimum of %d TB free" % minsize)

if (free // (2**30) / 1000) < minsize:
	print("Need to clean up!")
	for root, directories, files in os.walk(path):
		for dir in directories:
			timestamp = os.path.getmtime(os.path.join(root, dir))
			if (now - maxdays) > timestamp:
				try:
					print("Removing directory ", os.path.join(root,dir))
					shutil.rmtree(os.path.join(root,dir))
				except Exception as e:
					print(e)
