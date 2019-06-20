import requests
# import urllib.request
import time
import datetime
import re
from bs4 import BeautifulSoup
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# noinspection SpellCheckingInspection
bot = telepot.Bot('863130447:AAHNE6jdJKSFBgncPY-eqlmRDuTq6RG227s')


def get_html(url, tag):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.findAll(tag)


def get_race_attr(number):
    races_list = get_html("https://www.formula1.com/en/racing/2019.html", "article")
    race_attr = str(races_list[number]).split("\n")
    return race_attr


def get_results(n, url):
    pilots = get_html(url, 'tr')
    data_pattern = r">.+<"
    time_pattern = r">.{3,11}<"

    ######################################################

    attr = str(pilots[n]).split("\n")
    pos_re = re.search(data_pattern, attr[2])
    car_number_re = re.search(data_pattern, attr[3])
    name_re = re.search(data_pattern, attr[5])
    surname_re = re.search(data_pattern, attr[6])
    abbr_re = re.search(data_pattern, attr[7])
    team_re = re.search(data_pattern, attr[9])
    laps_re = re.search(data_pattern, attr[10])
    time_re = re.search(time_pattern, attr[11])
    pts_re = re.search(data_pattern, attr[12])

    ######################################################

    pos = pos_re.group()
    car_number = car_number_re.group()
    name = name_re.group()
    surname = surname_re.group()
    abbr = abbr_re.group()
    team = team_re.group()
    laps = laps_re.group()
    time = time_re.group()
    pts = pts_re.group()

    ######################################################

    result = {"pos": pos, "car_number": car_number, " name": name, "surname": surname,
              "abbr": abbr, "team": team, "laps": laps, "time": time, "pts": pts}
    return result


'''
def get_results_url(state):
    urlPattern   = r"\".{75,95}\""
    urlPattern2  = r".+[h][t][m][l]"
    racesUrl     = "https://www.formula1.com/en/racing/2019/"+state+".html"
    races        = get_html(racesUrl,'p')
    race         = str(races[14]).split("\n")
    rUrlRE       = re.search(urlPattern,race[9])
    rUrl         = rUrlRE.group()
    rUrl2RE      = re.search(urlPattern2,rUrl.replace("\"",""))
    rUrl2        = rUrl2RE.group()
    return(rUrl2)
'''


def get_results_url(state):
    return "https://www.formula1.com/en/results.html/2019/races/1000/" + state + "/race-result.html"


def month_to_number(month):
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    return months[month]


def get_state(number):
    state_pattern1 = r"/[A-Za-z]+\.jpg"
    state_pattern2 = r"[A-Za-z]+"
    state1 = re.search(state_pattern1, get_race_attr(number)[1])
    state2 = re.search(state_pattern2, state1.group())
    return state2.group()


def get_date(number):
    date_pattern = r"[0-9]{1,2} [A-Za-z]{3,3}"
    date_re = re.search(date_pattern, get_race_attr(number)[6])
    date_text = date_re.group().split(" ")
    num = int(date_text[0])
    month = month_to_number(date_text[1])
    date = [num, month]
    return date


def disputed_races():
    now = datetime.datetime.now()
    disputed = []
    print('Updating calendar......')
    for i in range(len(get_html("https://www.formula1.com/en/racing/2019.html", "article"))):
        date = get_date(i)
        if (now.month > date[1]) or ((now.month == date[1]) and (now.day > date[0])):
            disputed.append(i)
    print('Done')
    return disputed


disputedRacesList = disputed_races()


def get_results_number(number, n):
    return get_results(n, get_results_url(get_state(number)))


# print(get_state(disputed_races()[-1]+1))


'''''''''''''''''''''''''''''''''''''''''''''

Keyboard creation

'''''''''''''''''''''''''''''''''''''''''''''
start = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='latest', callback_data='latest'),
                                               InlineKeyboardButton(text='next', callback_data='next')],
                                              [InlineKeyboardButton(text='previous races', callback_data='previous')],
                                              [InlineKeyboardButton(text='upcoming races', callback_data='upcoming')]])


def result_keyboard(n):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 1)['abbr'],
            time=get_results_number(n, 1)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 2)['abbr'],
            time=get_results_number(n, 2)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 3)['abbr'],
            time=get_results_number(n, 3)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 4)['abbr'],
            time=get_results_number(n, 4)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 5)['abbr'],
            time=get_results_number(n, 5)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 6)['abbr'],
            time=get_results_number(n, 6)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 7)['abbr'],
            time=get_results_number(n, 7)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 8)['abbr'],
            time=get_results_number(n, 8)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 9)['abbr'],
            time=get_results_number(n, 9)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 10)['abbr'],
            time=get_results_number(n, 10)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 11)['abbr'],
            time=get_results_number(n, 11)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 12)['abbr'],
            time=get_results_number(n, 12)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 13)['abbr'],
            time=get_results_number(n, 13)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 14)['abbr'],
            time=get_results_number(n, 14)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 15)['abbr'],
            time=get_results_number(n, 15)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 16)['abbr'],
            time=get_results_number(n, 16)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 17)['abbr'],
            time=get_results_number(n, 17)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 18)['abbr'],
            time=get_results_number(n, 18)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 19)['abbr'],
            time=get_results_number(n, 19)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=get_results_number(n, 20)['abbr'],
            time=get_results_number(n, 20)['time']), callback_data='pilot')],
        [InlineKeyboardButton(text='<---back---', callback_data='start')]])


latest = result_keyboard(disputedRacesList[-1])

# print(get_results_number(disputedRacesList[-1],1)['abbr'], get_results_number(disputedRacesList[-1],1)['time'])
'''''''''''''''''''''''''''''''''''''''''''''
Telegram bot integration

'''''''''''''''''''''''''''''''''''''''''''''


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, 'Try pressing one of the buttons below', reply_markup=start)


def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)
    if query_data == 'latest':
        bot.sendMessage(chat_id, '{state} Grand Prix'.format(state=get_state(disputedRacesList[-1])),
                        reply_markup=latest)
        bot.answerCallbackQuery(query_id)
    elif query_data == 'start':
        bot.sendMessage(chat_id, 'Try pressing one of the buttons below', reply_markup=start)
        bot.answerCallbackQuery(query_id)


i = 0

MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()

while 1:
    time.sleep(1)
    i += 1
    print(i)
    if i >= 3600:
        i = 0
        disputedRacesList = disputed_races()
        latest = result_keyboard(disputedRacesList[-1])
