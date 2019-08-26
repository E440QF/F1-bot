import requests                                                             #
import time                                                                 #
import datetime                                                             #
import re                                                                   #
from bs4 import BeautifulSoup                                               # Importing modules
import telepot                                                              # needed by this program
from telepot.loop import MessageLoop                                        #
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton   #
from modules.database import User, Race                                     #
from pony.orm import db_session                                             #


try:
    f = open('token.txt', 'r')                          #
    token = f.readline().strip()                        #
    f.close()                                           #
except FileNotFoundError:                               # Getting the telegram bot token
    token = input("write here the bot api token: ")     # from user/token.txt
    f = open('token.txt', 'w')                          #
    f.write(token)                                      #
    f.close()                                           #
                                                        #
bot = telepot.Bot(token)                                # Telegram bot object initialization


def get_html(url, tag):                                 #
    response = requests.get(url)                        # This function returns all the occourrencies
    soup = BeautifulSoup(response.text, "html.parser")  # of a specific tag in the url's html
    return soup.findAll(tag)                            #


def get_race_attr(number):                              #
    races_list = get_html("https://www.formula1.com"    # This function returns all the attributes needed by 
                    "/en/racing/2019.html", "article")  # the program for a specified race
    race_attr = str(races_list[number]).split("\n")     #
    return race_attr                                    #


def get_results(n, url, pilots):
    if pilots is None:
        pilots = get_html(url, 'tr')

    data_pattern = r">.+<"                              # REGEX pattern used for the scraping of regular data
    time_pattern = r">.{2,11}<"                         # REGEX pattern used for the scraping of time data

    #####################################################

    attr = str(pilots[n]).split("\n")                   #
    pos_re = re.search(data_pattern, attr[2])           #
    car_number_re = re.search(data_pattern, attr[3])    #
    name_re = re.search(data_pattern, attr[5])          #
    surname_re = re.search(data_pattern, attr[6])       # This piece of code searches for pilot data using
    abbr_re = re.search(data_pattern, attr[7])          # the previously mentioned REGEX patterns
    team_re = re.search(data_pattern, attr[9])          #
    laps_re = re.search(data_pattern, attr[10])         #
    time_re = re.search(time_pattern, attr[11])         #
    pts_re = re.search(data_pattern, attr[12])          #

    #####################################################

    pos = pos_re.group()                                #
    car_number = car_number_re.group()                  #
    name = name_re.group()                              #
    surname = surname_re.group()                        # This piece of code extract the data from the
    abbr = abbr_re.group()                              # results of the REGEX search
    team = team_re.group()                              #
    laps = laps_re.group()                              #
    time = time_re.group()                              #
    pts = pts_re.group()                                #

    #####################################################

    result = [pos, car_number, name, surname, abbr, team, laps, time, pts]      # This function returns the
                                                                                # results for a given pilot
    return result                                                               # on a given race


def get_results_url(state, n):                                                  # This is the actual code that gets the
    return "https://www.formula1.com/en/results.html/2019/races/" + \
           str(1000 + n) + "/" + state.replace("_", "-") + "/race-result.html"  # url of the results of a specified race


def month_to_number(month):                                                     #
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,       # This function converts literal
              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}    # months into numerical months
    return months[month]                                                        #


def get_state(number):                                                          #
    state_pattern1 = r"/[A-Za-z_]+\.jpg"                                        #
    state_pattern2 = r"[A-Za-z_]+"                                              # This function returns the
    state1 = re.search(state_pattern1, get_race_attr(number)[1])                # state of a race requiring the
    state2 = re.search(state_pattern2, state1.group())                          # number of the race as input
    return state2.group()                                                       #


def get_date(number):                                                           #
    date_pattern = r"[0-9]{1,2} [A-Za-z]{3,3}"                                  #
    date_re = re.search(date_pattern, get_race_attr(number)[6])                 # This function returns the
    date_text = date_re.group().split(" ")                                      # date of a race requiring the
    num = int(date_text[0])                                                     # umber of the race as input
    month = month_to_number(date_text[1])                                       #
    date = [num, month]                                                         #
    return date                                                                 #

def disputed_races():                                                                   #
    now = datetime.datetime.now()                                                       #
    disputed = []                                                                       #
    print('Updating calendar......')                                                    #
    length = len(get_html("https://www.formula1.com/en/racing/2019.html", "article"))   # This function returns a list
    for j in range(length):                                                             # containing all the races that
        date = get_date(j)                                                              # have already been disputed
        if (now.month > date[1]) or ((now.month == date[1]) and (now.day > date[0])):   #
            disputed.append(j)                                                          #
    print('Done')                                                                       #
    return disputed                                                                     #


@db_session
def update_race_database():
    for number in disputedRacesList:
        if not Race.exists(lambda n: n.number == number):
            Race(number=number)
            race  = Race.get(number=number)

            n01   = get_results_number(number,  1)
            print("getting reslts")
            n02   = get_results_number(number,  2)
            print("getting reslts")
            n03   = get_results_number(number,  3)
            print("getting reslts")
            n04   = get_results_number(number,  4)
            print("getting reslts")
            n05   = get_results_number(number,  5)
            print("getting reslts")
            n06   = get_results_number(number,  6)
            print("getting reslts")
            n07   = get_results_number(number,  7)
            print("getting reslts")
            n08   = get_results_number(number,  8)
            print("getting reslts")
            n09   = get_results_number(number,  9)
            print("getting reslts")
            n10   = get_results_number(number, 10)
            print("getting reslts")
            n11   = get_results_number(number, 11)
            print("getting reslts")
            n12   = get_results_number(number, 12)
            print("getting reslts")
            n13   = get_results_number(number, 13)
            print("getting reslts")
            n14   = get_results_number(number, 14)
            print("getting reslts")
            n15   = get_results_number(number, 15)
            print("getting reslts")
            n16   = get_results_number(number, 16)
            print("getting reslts")
            n17   = get_results_number(number, 17)
            print("getting reslts")
            n18   = get_results_number(number, 18)
            print("getting reslts")
            n19   = get_results_number(number, 19)
            print("getting reslts")
            n20   = get_results_number(number, 20)
            print("getting reslts")
            date  = get_date(number)
            state = get_state(number)
            print('setting')
            race.set(n01=n01, n02=n02, n03=n03, n04=n04, n05=n05, n06=n06, n07=n07, n08=n08, n09=n09,
                     n10=n10, n11=n11, n12=n12, n13=n13, n14=n14, n15=n15, n16=n16, n17=n17,
                     n18=n18, n19=n19, n20=n20, date=date, state=state, disputed=True)
            print('set')

@db_session
def db_to_results(number):
    race = Race.get(number = number)
    return [race.n01, race.n02, race.n03, race.n04, race.n05, race.n06, race.n07, race.n08, race.n09, race.n10,
            race.n11, race.n12, race.n13, race.n14, race.n15, race.n16, race.n17, race.n18, race.n19, race.n20,
            race.state, race.date]


def get_results_number(number, n, pilots=None):                                 # This function shortens the process
    return get_results(n, get_results_url(get_state(number), number), pilots)   # of getting results from  race number

'''''''''''''''''''''''''''''''''''''''''''''

Keyboard creation

'''''''''''''''''''''''''''''''''''''''''''''
start = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='latest', callback_data='latest'),
                                               InlineKeyboardButton(text='next', callback_data='next')],
                                              [InlineKeyboardButton(text='previous races', callback_data='previous')],
                                              [InlineKeyboardButton(text='upcoming races', callback_data='upcoming')]])

@db_session
def previous_keyboard():
    buttons = []

    for r in disputedRacesList:
        buttons.append([InlineKeyboardButton(text='{race}: {state}'.format(race=str(r+1),
                                            state=db_to_results(r)[20]),callback_data=str(r))])

    buttons.append([InlineKeyboardButton(text='<---back---', callback_data='start')])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def result_keyboard(n,callback='start'):
    results = db_to_results(n)
    buttons = []

    for p in range(11):
        buttons.append([InlineKeyboardButton(text="{num}: {abbr}  {time}".format(
                                            num=p+1,
                                            abbr=results[p][4],
                                            time=results[p][7]), callback_data='pilot'),
                        InlineKeyboardButton(text="{num}: {abbr}  {time}".format(
                                            num=p+2,
                                            abbr=results[p+1][4],
                                            time=results[p+1][7]), callback_data='pilot')])

    buttons.append([InlineKeyboardButton(text='<---back---', callback_data=callback)])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def update_data():
    global latest
    global disputedRacesList
    global previous
    disputedRacesList = disputed_races()
    update_race_database()
    latest = result_keyboard(disputedRacesList[-1])
    previous = previous_keyboard()

update_data()
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
        bot.sendMessage(chat_id,
                        '{state} Grand Prix, {day}/{month}/2019'.format(state=db_to_results(disputedRacesList[-1])[20],
                                                                    day=db_to_results(disputedRacesList[-1])[21][0],
                                                                    month=db_to_results(disputedRacesList[-1])[21][1]),
                        reply_markup=latest)
        bot.answerCallbackQuery(query_id)
    elif query_data == 'start':
        bot.sendMessage(chat_id, 'Try pressing one of the buttons below', reply_markup=start)
        bot.answerCallbackQuery(query_id)
    elif query_data == 'previous':
        bot.sendMessage(chat_id, 'Previous races', reply_markup=previous)
        bot.answerCallbackQuery(query_id)
    elif re.match("[0-9]+", query_data):
        bot.sendMessage(chat_id,  '{state} Grand Prix, {day}/{month}/{year}'.format(
                                                        state=db_to_results(disputedRacesList[int(query_data)])[20],
                                                        day=db_to_results(disputedRacesList[int(query_data)])[21][0],
                                                        month=db_to_results(disputedRacesList[int(query_data)])[21][1],
                                                        year=datetime.datetime.now().year),
                        reply_markup=result_keyboard(int(query_data), 'previous'))
        bot.answerCallbackQuery(query_id)


MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()


i = 0
while 1:
    time.sleep(1)
    i += 1
    print(i)
    if i >= 3600:
        i = 0
        update_data()
