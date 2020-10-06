import sys
from PIL import Image
import os
from os import listdir
from os.path import isfile, join
Pas=256
for element in os.listdir("BDDG/BDDO"): 
	if not element.endswith(".jpg"): continue
	im = Image.open(os.path.join("BDDG/BDDO",element))
	ima=im.resize([Pas,Pas])
	ima.save("BDDG/BDD256/"+element, "JPEG")


	