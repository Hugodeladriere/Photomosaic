import sys
from PIL import Image
import os
from os import listdir
from os.path import isfile, join

d=0
for element in os.listdir("BDDG/BDD512/"):
		if not element.endswith(".jpg"): continue
		im = Image.open("BDDG/BDD512/" +element)
		name = str(d)+".jpg"
		im.save("BDDG/BDD512/" + name, "JPEG")
		d+=1
