import os
import sys

root_dir = "./static/images"
with open("./data.sql","w") as fw:
	for root, dirs, files in os.walk(root_dir, onerror=None):
	    for filename in files:
	    		b = filename.split(".")
	    		a = b[0].split("_")
	    		name = " ".join(a)
	    		s = "INSERT INTO `images` (`filename`, `name`) VALUES " + "('" +filename+"','"+name+"');"
			fw.write(s)
			fw.write("\n")
