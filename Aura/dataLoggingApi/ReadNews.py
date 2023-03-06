import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import pyttsx3
from datetime import datetime
from dateutil import parser

engine = pyttsx3.init()  # SETUP AND SETTING VOICE
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1)
engine.setProperty('voice', voices[0].id)

started = "Started fetching yours favorite news today"
engine.say(started)
engine.runAndWait()

Favorites = pd.read_csv('rank.csv')
df = pd.DataFrame(Favorites)
Top_News = []
Favorites_News = {5: [], 4: [], 3: [], 2: [], 1: []}


def recent(date):
    timestamp = datetime.now()
    day = str(timestamp).split(" ")[0]
    today = parser.parse(day)
    checkDate = parser.parse(date)
    txt = today - checkDate
    recentness = re.findall("(\d+) day,", str(txt))
    if len(recentness) == 0:
        recentness = re.findall("(\d+) days,", str(txt))

    try:
        if int(recentness[0]) <= 2:
            return True
        else:
            return False
    except:
        return True


def getNews(category):
    global ne, fav, con
    newsDictionary = {
        'success': True,
        'category': category,
        'data': []
    }

    try:
        htmlBody = requests.get('https://www.inshorts.com/en/' + category)
    except:
        print("something went wrong")

    soup = BeautifulSoup(htmlBody.text, 'lxml')
    newsCards = soup.find_all(class_='news-card')
    if not newsCards:
        newsDictionary['success'] = False
        newsDictionary['errorMessage'] = 'Invalid Category'
        return newsDictionary

    for card in newsCards:
        try:
            title = card.find(class_='news-card-title').find('a').text
        except AttributeError:
            title = None

        try:
            content = card.find(class_='news-card-content').find('div').text
        except AttributeError:
            content = None
        try:
            date = card.find(clas='date').text
        except AttributeError:
            date = None

        try:
            time = card.find(class_='time').text
        except AttributeError:
            time = None

        newsObject = {
            'title': title,
            'content': content.lower(),
            'date': date + "|" + time,
        }
        # print(category+"|||"+ str(date) +"||"+title)
        if recent(date):
            for i in range(int(df.shape[0])):  # int(df.shape[0])):
                if (content).find(str(df.loc[i, 'Key'])) != -1:
                    # print( int(df.loc[i, 'Rank']),"|"+str(df.loc[i, 'Key'])+"||"+date+"||"+"|" ,content ,)
                    Favorites_News[int(df.loc[i, 'Rank'])].append(content)

                    break
        else:
            pass

        newsDictionary['data'].append(newsObject)


mk = ['sports', 'technology', 'startup', 'entertainment', 'science', 'automobile']  # ['sports','entertainment',]
for i in mk:
    daata = getNews('read/' + i)


for r in range(1, 6):  # 1 , 6 are ranks
    for i in range(len(Favorites_News[r])):
        if str(Favorites_News[r][i]) not in Top_News:
            Top_News.append(Favorites_News[r][i])


def read(news, Top):
    counter = 1
    for i in range(1, (Top)):
        print(Top_News[-i])
        speech = "News" + str(counter) + ", " + str(Top_News[-i]) + ", "
        engine.say(speech)
        engine.runAndWait()
        counter = counter + 1


if len(Top_News) > 6:  # if news is > 6 then read only top 6
    read(Top_News, 7)
else:
    read(Top_News, len(Top_News))

speech = "That's the News Today Sir "
engine.say(speech)
engine.runAndWait()
#