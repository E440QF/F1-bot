import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup
def getHtml(url,tag):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	return(soup.findAll(tag))
def getResults(n,url):
	pilots = getHtml(url,'tr')
	dataPattern  = r">.+<"
	timePattern  = r">.{3,11}<"
######################################################
	attr        = str(pilots[n]).split("\n")
	posRE       = re.search(dataPattern, attr[2])
	carNumberRE = re.search(dataPattern, attr[3])
	nameRE      = re.search(dataPattern, attr[5])
	surnameRE   = re.search(dataPattern, attr[6])
	abbrRE      = re.search(dataPattern, attr[7])
	#####teamRE      = re.search(dataPattern, attr[9])
	lapsRE      = re.search(dataPattern, attr[10])
	timeRE      = re.search(timePattern, attr[11])
	ptsRE       = re.search(dataPattern, attr[12])
######################################################
	pos         = posRE.group()
	carNumber   = carNumberRE.group()
	name        = nameRE.group()
	surname     = surnameRE.group()
	abbr        = abbrRE.group()
	team        = teamRE.group()
	laps        = lapsRE.group()
	time        = timeRE.group()
	pts         = ptsRE.group()
######################################################
	result      = {"pos":pos,"carNumber":carNumber,"name":name,"surname":surname,"abbr":abbr,"team":team,"laps":laps,"time":time,"pts":pts}
	return(result)
def getResultsUrl(state):
	urlPattern = r"\".{75,95}\""
	racesUrl = "https://www.formula1.com/en/racing/2019/"+state+".html"
	races = getHtml(racesUrl,'p')
	race =str(races[14]).split("\n")
	rUrlRE = re.search(urlPattern,race[9])
	rUrl = rUrlRE.group()
	return(rUrl.replace("\"",""))
#def getRace(n)
#print(getHtml('https://www.formula1.com/en/racing/2019.html','article')[0])
#print(getResults(1,getResultsUrl("China")))


