import sys
from PIL import Image
from PIL import ImageEnhance
from PIL import ImagePalette
import os
import time
from os import listdir
#from os.path import isfile, join
import math



debut = time.time()

Pas=28
DecoupageG="Decoupageg/Decoupagehero/"
BDD="BDDG/BDDra28/"
preselc = "preselc/preselc16/"


def Decoupage():
	#d=0
	#cord = []
	#mypath = "Decoupage"
	#if len(sys.argv)>2: mypath = "Decoupage"
	#onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".jpg")]


	im = Image.open(sys.argv[1])
	imr = im.resize([4320,2700])
	hauteur = imr.size[1]
	largeur = imr.size[0]
	for x in range(0,largeur,Pas):
		for y in range(0,hauteur,Pas):
			im2 = imr.crop((x,y,x+Pas,y+Pas))
			name = str((x,y))+".jpg" # renome le nom de chaque image en fonction de ses coords 
			im2.save(DecoupageG + name, "JPEG")
			#cord.append((x,y))
			
			#print(cord[d])
			
			#d+=1
	#print(cord)
	#return cord



def norm(histo):
	s = sum(histo)
	return [z*100/s for z in histo]
		

def calculhisto(im):
	return  norm(im.histogram())

def calculate_median(l):
    l.sort()
    median = l[len(l)//2]
    return median





def histolenna():
	histolenna = {} #dictionnaire qui associe le nom de l'image a sa valeur de son histogramme 
	for element in sorted(os.listdir(DecoupageG)):
		if not element.endswith(".jpg"): continue
		im = Image.open(DecoupageG +element)
		histolenna[element] = (calculhisto(im))
	print("len histo lenna ", len(histolenna))
	return histolenna

def histoBDD():
	histoBDD = {}
	for element in sorted(os.listdir(BDD)):
		if not element.endswith(".jpg"): continue
		im =Image.open(BDD+element)

		histoBDD[element] = (calculhisto(im))
	print("histo BDDd len ", len(histoBDD))
	return histoBDD

def histolennaHSV():
	histolennaHSV= {} #dictionnaire qui associe le nom de l'image a sa valeur de son histogramme 
	for element in sorted(os.listdir(DecoupageG)):
		if not element.endswith(".jpg"): continue
		im = Image.open(DecoupageG +element).convert("RGB").convert("HSV")
		histolennaHSV[element] = (calculhisto(im))
	print("len histo  HSV ", len(histolennaHSV))
	return histolennaHSV

def histoBDDHSV():
	histoBDDHSV = {}
	for element in sorted(os.listdir(BDD)):
		if not element.endswith(".jpg"): continue
		im =Image.open(BDD+element).convert("RGB").convert("HSV")

		histoBDDHSV[element] = (calculhisto(im))
	print("histo BDDd len HSV ", len(histoBDDHSV))
	return histoBDDHSV




def calculDiff(cord,histolenna,histoBDD,histolennaHSV,histoBDDHSV):
	#Initialisation du dictinnaire 
	mini_indice={}

	

	#for element in sorted(os.listdir(DecoupageG)): 
		#if not element.endswith(".jpg"): continue
		#print("elllllllleeeement )", element)

	for element in sorted(os.listdir(DecoupageG)): 
		if not element.endswith(".jpg"): continue		
		mini = 20000000000000000000000000000000
		string ="nul"

		histL = histolenna[element]
		histLHSV =histolennaHSV[element]
		#print("          	" ,histL)
		for elementBDD in sorted(os.listdir(BDD)):
			if not elementBDD.endswith(".jpg"): continue


			histB = histoBDD[elementBDD]
			histBHSV= histoBDDHSV[elementBDD]
			diffH = sum(abs(x-y) for x,y in zip(histL, histB))
			diffH += sum((abs(x-y)/6) for x,y in zip(histLHSV, histBHSV))

			#print (element, elementBDD, diffH)




			if( diffH < mini):
				mini= diffH
				string=elementBDD
			
		#print("stringfinal      ",string)
		mini_indice[element]=string
		#string = nom de l'image qui ressemble le plus a l'image tester 
		#im= Image.open(preselc + string)
		#im.save("preselc/preselcsauv/"+string, "JPEG")
		#os.remove(preselc+string)

		
		
		
		#images.append("%d.jpg"%minimum)
		#print(minimum)
				
		#print("indice", r)
	#histmin.append(mini) 
	print(len(mini_indice))
	#print("mini indice ", mini_indice)
	#print("longuer images.             ",len(images))
	#print(images)



	return mini_indice

def coord(string):
	
	liste  = string.replace("(","")
	liste =  liste.replace(").jpg","")
	liste = liste.split(",")
	#x= liste[0]
	#y = liste[1]

	return (liste)



def medianeRGB():
	pic={}
	liste=[]
	for element in os.listdir("Decoupageg/Decoupage64/"): 
		if not element.endswith(".jpg"): continue
		im = Image.open(os.path.join("Decoupageg/Decoupage64/",element))
		haut = im.size[0]
		for x in range(haut):
			for y in range(haut):
				pix = im.load()
				value= pix[x,y]
				liste.append(value)
		mediane = calculate_median(liste)
		pic[element]= mediane		
	return pic

def repixeliser(dico):
	for cle, value in dico.iteritems():
		im = Image.open("Decoupageg/Decoupage64/",cord)
		ima = ImagePalette.ImagePalette("RGB",value,0)







def coller(mini_indice):
	im = Image.open(sys.argv[1])
	final = Image.new("RGB", [4320,2700], color=(0,0,0) )
	#for x in range(0,1024,Pas):
		#for y in range(0,1024,Pas):

	for cle , valeur in mini_indice.iteritems() :
		#print(cle)

		cord = coord(cle)
		x = int(cord[0])
		y = int(cord[1])


		#print(x,y)

		#print(valeur)
	#name = "im_"+str((x,y))+".jpg"
		im = Image.open(BDD+valeur)
		#augmente le contraste en suppriment les extrimites de l'histo (cutoff)
		#ima = ImageOps.autocontrast(im, cutoff=3, ignore=None) 
		#diminue la luminosite avec un coefficient enhance : 0.0 black/ 1.0 original
		#ima = ImageEnhance.Brightness(im).enhance(0.7)	 
		#imag = ImageEnhance.Sharpness(ima).enhance(5)
		


		final.paste(im,(x,y,x+Pas,y+Pas))

		
			
	final.show()
	name = "avangersfinal"
	final.save("final/"+name,"JPEG")



#preselec()




coller(calculDiff(Decoupage(),histolenna(),histoBDD(),histolennaHSV(),histoBDDHSV()))

fin = time.time()

print("temps d'execution : ", fin - debut)


