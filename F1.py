import requests
import urllib.request
import time
import datetime
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
	teamRE      = re.search(dataPattern, attr[9])
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

def monthToNumber(month):
	months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
	return(months[month])

statePattern1  = r"[0-9]{4,4}/[A-Za-z]+/_jcr"
statePattern2 = r"[A-Za-z]+"
racesList = getHtml("https://www.formula1.com/en/racing/2019.html","article")
raceAttr = str(racesList[1]).split("\n")
print(raceAttr[12])
state1 = re.search(statePattern1,raceAttr[1])
state2 = re.search(statePattern2,state1.group())
#print(state2.group())
monthPattern = r"[A-Z][a-z][a-z]"
now = datetime.datetime.now()
month = re.search(monthPattern,raceAttr[12])
print(now.month)
print(monthToNumber(month.group()))
