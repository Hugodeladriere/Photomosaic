import sys
from PIL import Image
import os
from os import listdir
from os.path import isfile, join


#def preselec():
#	histopreselec =[]
#	im = Image.open("lena.jpg")
#	hist1=calculhisto(im)

#	for element in os.listdir("BDD/"):
#		im1 = Image.open(os.path.join("BDD/",element))
#		if (calculDiff(hist1,calculhisto(im1)) < 150 ):
#			im1.save("preselec/"+element, "JPEG")



	
Pas=256
DecoupageG="Decoupageg/Decoupage256/"
BDD="BDDG/BDD2566/"


def Decoupage():
	d=0
	#mypath = "Decoupage"
	#if len(sys.argv)>2: mypath = "Decoupage"
	#onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".jpg")]

	im = Image.open(sys.argv[1])
	imr = im.resize([1024,1024])
	hauteur = imr.size[1]
	largeur = imr.size[0]
	for x in range(0,largeur,Pas):
		for y in range(0,hauteur,Pas):
			im2 = imr.crop((x,y,x+Pas,y+Pas))
			name = "im_"+str(d)+".jpg"
			im2.save(DecoupageG + name, "JPEG")
			d+=1


def norm(histo):
	s = sum(histo)
	return [z*100/s for z in histo]
		

def calculhisto(im):
	return  norm(im.histogram())



def histolenna():
	histolenna = []
	for element in sorted(os.listdir(DecoupageG)):
		if not element.endswith(".jpg"): continue
		im = Image.open(DecoupageG +element)
		histolenna.append(calculhisto(im))

	return histolenna
	

def histoBDD():
	histoBDD = []
	for element in sorted(os.listdir(BDD)):
		if not element.endswith(".jpg"): continue
		im =Image.open(BDD+element)
		histoBDD.append(calculhisto(im))

	return histoBDD


def calculDiff(histolenna,histoBDD):
	images=[]
	histmin = []
	r=0
	for element in os.listdir(DecoupageG): continue
	for k in range(0,len(histolenna)):
		mini = 20000000;
		histL = histolenna[k]
		for c in range (0,len(histoBDD)):
			histB = histoBDD[c]

			diffH = sum(abs(x-y) for x,y in zip(histB, histL))
			print (k, c,diffH)
			
			if( diffH < mini):
				mini= diffH
				r=c
				#print(r)
		images.append("%d.jpg"%r)

			
			
		#print("mini", diffH)
	histmin.append(mini) 
	print("fiinal.                 ",r)
	print("longuer images.             ",len(images))
	return images


def coler(images):
	d=0	
	final = Image.new("HSV", [1024,1024], color=(0,0,0) )
	for x in range(0,1024,Pas):
		for y in range(0,1024,Pas):
			im = Image.open(BDD + images[d])
			final.paste(im,(x,y,x+Pas,y+Pas))
			d+=1

	final.show()

#preselec()

Decoupage()
coler(calculDiff(histolenna(),histoBDD()))




