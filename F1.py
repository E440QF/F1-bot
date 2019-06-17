import requests
import urllib.request
import time
import datetime
import re
from bs4 import BeautifulSoup
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot('863130447:AAHNE6jdJKSFBgncPY-eqlmRDuTq6RG227s')

def getHtml(url,tag):
	response     = requests.get(url)
	soup         = BeautifulSoup(response.text, "html.parser")
	return(soup.findAll(tag))

def getRaceAttr(number):
	racesList    = getHtml("https://www.formula1.com/en/racing/2019.html","article")
	raceAttr     = str(racesList[number]).split("\n")
	return(raceAttr)

def getResults(n,url):
	pilots       = getHtml(url,'tr')
	dataPattern  = r">.+<"
	timePattern  = r">.{3,11}<"
######################################################
	attr         = str(pilots[n]).split("\n")
	posRE        = re.search(dataPattern, attr[2])
	carNumberRE  = re.search(dataPattern, attr[3])
	nameRE       = re.search(dataPattern, attr[5])
	surnameRE    = re.search(dataPattern, attr[6])
	abbrRE       = re.search(dataPattern, attr[7])
	teamRE       = re.search(dataPattern, attr[9])
	lapsRE       = re.search(dataPattern, attr[10])
	timeRE       = re.search(timePattern, attr[11])
	ptsRE        = re.search(dataPattern, attr[12])
######################################################
	pos          = posRE.group()
	carNumber    = carNumberRE.group()
	name         = nameRE.group()
	surname      = surnameRE.group()
	abbr         = abbrRE.group()
	team         = teamRE.group()
	laps         = lapsRE.group()
	time         = timeRE.group()
	pts          = ptsRE.group()
######################################################
	result       = {"pos":pos,"carNumber":carNumber,"name":name,"surname":surname,"abbr":abbr,"team":team,"laps":laps,"time":time,"pts":pts}
	return(result)
'''
def getResultsUrl(state):
	urlPattern   = r"\".{75,95}\""
	urlPattern2  = r".+[h][t][m][l]"
	racesUrl     = "https://www.formula1.com/en/racing/2019/"+state+".html"
	races        = getHtml(racesUrl,'p')
	race         = str(races[14]).split("\n")
	rUrlRE       = re.search(urlPattern,race[9])
	rUrl         = rUrlRE.group()
	rUrl2RE      = re.search(urlPattern2,rUrl.replace("\"",""))
	rUrl2        = rUrl2RE.group()
	return(rUrl2)
'''
def getResultsUrl(state):
	return("https://www.formula1.com/en/results.html/2019/races/1000/"+state+"/race-result.html")

def monthToNumber(month):
	months       = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
	return(months[month])

def getState(number):
	statePattern1  = r"/[A-Za-z]+\.jpg"
	statePattern2 = r"[A-Za-z]+"
	state1 = re.search(statePattern1,getRaceAttr(number)[1])
	state2 = re.search(statePattern2,state1.group())
	return(state2.group())

def getDate(number):
	attr = getRaceAttr(number)
	datePattern = r"[0-9]{1,2} [A-Za-z]{3,3}"
	dateRE = re.search(datePattern,getRaceAttr(number)[6])
	dateText = dateRE.group().split(" ")
	num = int(dateText[0])
	month = monthToNumber(dateText[1])
	date = [num,month]
	return(date)

def disputedRaces():
	now = datetime.datetime.now()
	disputed = []
	print('Updating calendar......')
	for i in range(len(getHtml("https://www.formula1.com/en/racing/2019.html","article"))):
		date = getDate(i)
		if((now.month > date[1]) or ((now.month == date[1]) and (now.day > date[0]))):
			disputed.append(i)
	print('Done')
	return(disputed)
disputedRacesList=disputedRaces()

def getResultsNumber(number,n):
	return(getResults(n,getResultsUrl(getState(number))))

#print(getState(disputedRaces()[-1]+1))


'''''''''''''''''''''''''''''''''''''''''''''

Keyboard creation

'''''''''''''''''''''''''''''''''''''''''''''
start  = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='latest', callback_data='latest'), InlineKeyboardButton(text='next', callback_data='next')],
							 				  					[InlineKeyboardButton(text='previous races', callback_data='previous')],
											  					[InlineKeyboardButton(text='upcoming races', callback_data='upcoming')]])

latest =  InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],1)['abbr'], time=getResultsNumber(disputedRacesList[-1],1)['time']),callback_data='pilot')],
											   	[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],2)['abbr'], time=getResultsNumber(disputedRacesList[-1],2)['time']),callback_data='pilot')],
       							                [InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],3)['abbr'], time=getResultsNumber(disputedRacesList[-1],3)['time']),callback_data='pilot')],
						                     	[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],4)['abbr'], time=getResultsNumber(disputedRacesList[-1],4)['time']),callback_data='pilot')],
                        						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],5)['abbr'], time=getResultsNumber(disputedRacesList[-1],5)['time']),callback_data='pilot')],
              						           	[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],6)['abbr'], time=getResultsNumber(disputedRacesList[-1],6)['time']),callback_data='pilot')],
                        						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],7)['abbr'], time=getResultsNumber(disputedRacesList[-1],7)['time']),callback_data='pilot')],
                         						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],8)['abbr'], time=getResultsNumber(disputedRacesList[-1],8)['time']),callback_data='pilot')],
                        						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],9)['abbr'], time=getResultsNumber(disputedRacesList[-1],9)['time']),callback_data='pilot')],
                         						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],10)['abbr'], time=getResultsNumber(disputedRacesList[-1],10)['time']),callback_data='pilot')],
                        						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],11)['abbr'], time=getResultsNumber(disputedRacesList[-1],11)['time']),callback_data='pilot')],
                         						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],12)['abbr'], time=getResultsNumber(disputedRacesList[-1],12)['time']),callback_data='pilot')],
                        						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],13)['abbr'], time=getResultsNumber(disputedRacesList[-1],13)['time']),callback_data='pilot')],
                         						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],14)['abbr'], time=getResultsNumber(disputedRacesList[-1],14)['time']),callback_data='pilot')],
                        						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],15)['abbr'], time=getResultsNumber(disputedRacesList[-1],15)['time']),callback_data='pilot')],
                         						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],16)['abbr'], time=getResultsNumber(disputedRacesList[-1],16)['time']),callback_data='pilot')],
                        						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],17)['abbr'], time=getResultsNumber(disputedRacesList[-1],17)['time']),callback_data='pilot')],
                         						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],18)['abbr'], time=getResultsNumber(disputedRacesList[-1],18)['time']),callback_data='pilot')],
                        						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],19)['abbr'], time=getResultsNumber(disputedRacesList[-1],19)['time']),callback_data='pilot')],
                         						[InlineKeyboardButton(text="1: {abbr}  {time}".format(abbr=getResultsNumber(disputedRacesList[-1],20)['abbr'], time=getResultsNumber(disputedRacesList[-1],20)['time']),callback_data='pilot')]])

print(getResultsNumber(disputedRacesList[-1],1)['abbr'], getResultsNumber(disputedRacesList[-1],1)['time'])
'''''''''''''''''''''''''''''''''''''''''''''
Telegram bot integration

'''''''''''''''''''''''''''''''''''''''''''''
def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	bot.sendMessage(chat_id, 'Try pressing one of the buttons below', reply_markup=start)

def on_callback_query(msg):
	query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
	print(query_data)
	if(query_data == 'latest'):
		bot.sendMessage(chat_id, '{state} Grand Prix'.format(state=getState(disputedRacesList[-1])), reply_markup=latest)
		bot.answerCallbackQuery(query_id)
i=0

MessageLoop(bot, {'chat': on_chat_message,'callback_query': on_callback_query}).run_as_thread()

while 1:
	time.sleep(1)
	i += 1
	print(i)
	if(i >= 3600):
		i = 0
		disputedRacesList = disputedRaces()