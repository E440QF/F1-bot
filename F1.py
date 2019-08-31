# Import modules
from requests import get
from time import sleep
from datetime import datetime
from re import search
from bs4 import BeautifulSoup
from telepot import Bot, glance
from schedule import every, run_pending
from modules.database import User, Race, Data
from pony.orm import db_session
from modules import keyboards

bot = None


def get_html(url, tag):                                 #
    response = get(url)                                 # This function returns all the occourrencies
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
    pos_re = search(data_pattern, attr[2])           #
    car_number_re = search(data_pattern, attr[3])    #
    name_re = search(data_pattern, attr[5])          #
    surname_re = search(data_pattern, attr[6])       # This piece of code searches for pilot data using
    abbr_re = search(data_pattern, attr[7])          # the previously mentioned REGEX patterns
    team_re = search(data_pattern, attr[9])          #
    laps_re = search(data_pattern, attr[10])         #
    time_re = search(time_pattern, attr[11])         #
    pts_re = search(data_pattern, attr[12])          #

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

    result = {"pos": pos, "car_number": car_number, " name": name, "surname": surname,  # This function returns the
              "abbr": abbr, "team": team, "laps": laps, "time": time, "pts": pts}       # results for a given pilot
    return result                                                                       # on a given race


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
    state1 = search(state_pattern1, get_race_attr(number)[1])                # state of a race requiring the
    state2 = search(state_pattern2, state1.group())                          # number of the race as input
    return state2.group()                                                       #


def get_date(number):                                                           #
    date_pattern = r"[0-9]{1,2} [A-Za-z]{3,3}"                                  #
    date_re = search(date_pattern, get_race_attr(number)[6])                 # This function returns the
    date_text = date_re.group().split(" ")                                      # date of a race requiring the
    num = int(date_text[0])                                                     # umber of the race as input
    month = month_to_number(date_text[1])                                       #
    date = [num, month]                                                         #
    return date                                                                 #


def get_results_number(number, n, pilots):                                      # This function shortens the process
    return get_results(n, get_results_url(get_state(number), number), pilots)   # of getting results from  race number


def reply(msg):
    chatId = msg['from']['id']
    name = msg['from']['first_name']
    sent = bot.sendMessage(chatId, "Hey, <b>{}</b>!\n"
                                   "What would you like to see?".format(name), parse_mode="HTML")
    bot.editMessageReplyMarkup((chatId, sent['message_id']), keyboards.start(sent['message_id']))


def inlinebutton(msg):
    chatId, query_data = glance(msg, flavor="callback_query")[1:3]
    user = User.get(chatId=chatId)
    data = Data.get(general=True)
    query_split = query_data.split("#")
    message_id = int(query_split[1])
    button = query_split[0]

    if button == "latest":
        results = [0]
        n = data.disputedRaces[-1]
        pilots = get_html(get_results_url(get_state(n), n), 'tr')
        for num in range(1, 21):
            results.append(get_results_number(n, num, pilots))
        message = ""
        for res in results:
            message += "- {}: {}".format(res['abbr'], res['time'])
        
        bot.editMessageText((chatId, message_id), "🏎 {} Grand Prix\n"
                                                  "{}".format(get_state(n), message), reply_markup=keyboards.back(message_id))

    elif button == "start":
        bot.editMessageText((chatId, message_id), "What would you like to see?", reply_markup=keyboards.start(message_id))

    else:
        bot.editMessageText((chatId, message_id), "Sorry, this function is currently not available.", reply_markup=None)


@db_session
def fetchRaces():
    data = Data.get(general=True)
    now = datetime.now()
    disputed = []
    length = len(get_html("https://www.formula1.com/en/racing/2019.html", "article"))
    for i in range(length):
        date = get_date(i)
        if (now.month > date[1]) or ((now.month == date[1]) and (now.day > date[0])):
            disputed.append(i)
    data.disputedRaces = disputed


@db_session
def initialize():
    if not Data.exists(lambda d: d.general == True):
        Data(general=True)
    fetchRaces()

    try:
        f = open('token.txt', 'r')
        token = f.readline().strip()
        f.close()
    except FileNotFoundError:
        token = input("Paste the bot API Token: ")
        f = open('token.txt', 'w')
        f.write(token)
        f.close()

    bot = Bot(token)


bot.message_loop({'chat': reply, 'callback_query': inlinebutton})
every().hour().do(fetchRaces)
initialize()

while True:
    sleep(60)
    run_pending()
