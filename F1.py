import requests
# import urllib.request
import time
import datetime
import re
from bs4 import BeautifulSoup
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from modules.database import User, Race

try:
    f = open('token.txt', 'r')
    token = f.readline().strip()
    f.close()
except FileNotFoundError:
    token = input("scrivi qui il token del bot: ")
    f = open('token.txt', 'w')
    f.write(token)
    f.close()

bot = telepot.Bot(token)


def get_html(url, tag):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.findAll(tag)


def get_race_attr(number):
    races_list = get_html("https://www.formula1.com/en/racing/2019.html", "article")
    race_attr = str(races_list[number]).split("\n")
    return race_attr


def get_results(n, url, pilots):
    if pilots is None:
        pilots = get_html(url, 'tr')

    data_pattern = r">.+<"
    time_pattern = r">.{2,11}<"

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

    result = [pos, car_number, name, surname, abbr, team, laps, time, pts]

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


def get_results_url(state, n):
    return "https://www.formula1.com/en/results.html/2019/races/" + \
           str(1000 + n) + "/" + state.replace("_", "-") + "/race-result.html"


def month_to_number(month):
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    return months[month]


def get_state(number):
    state_pattern1 = r"/[A-Za-z_]+\.jpg"
    state_pattern2 = r"[A-Za-z_]+"
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
    length = len(get_html("https://www.formula1.com/en/racing/2019.html", "article"))
    for j in range(length):
        date = get_date(j)
        if (now.month > date[1]) or ((now.month == date[1]) and (now.day > date[0])):
            disputed.append(j)
    print('Done')
    return disputed


disputedRacesList = disputed_races()


def get_results_number(number, n, pilots):
    return get_results(n, get_results_url(get_state(number), number), pilots)


# print(get_state(disputed_races()[-1]+1))


'''''''''''''''''''''''''''''''''''''''''''''

Keyboard creation

'''''''''''''''''''''''''''''''''''''''''''''
start = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='latest', callback_data='latest'),
                                               InlineKeyboardButton(text='next', callback_data='next')],
                                              [InlineKeyboardButton(text='previous races', callback_data='previous')],
                                              [InlineKeyboardButton(text='upcoming races', callback_data='upcoming')]])


def result_keyboard(n):
    results = [0]
    pilots = get_html(get_results_url(get_state(n), n), 'tr')

    for num in range(1, 21):
        print('getting ' + str(num) + ' results')
        results.append(get_results_number(n, num, pilots))

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[1][4],
            time=results[1][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[2][4],
            time=results[2][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[3][4],
            time=results[3][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[4][4],
            time=results[4][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[5][4],
            time=results[5][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[6][4],
            time=results[6][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[7][4],
            time=results[7][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[8][4],
            time=results[8][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[9][4],
            time=results[9][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[10][4],
            time=results[10][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[11][4],
            time=results[11][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[12][4],
            time=results[12][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[13][4],
            time=results[13][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[14][4],
            time=results[14][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[15][4],
            time=results[15][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[16][4],
            time=results[16][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[17][4],
            time=results[17][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[18][4],
            time=results[18][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[19][4],
            time=results[19][7]), callback_data='pilot')],
        [InlineKeyboardButton(text="1: {abbr}  {time}".format(
            abbr=results[20][4],
            time=results[20][7]), callback_data='pilot')],
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

