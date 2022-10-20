from flask import Flask, jsonify, request, abort
import requests
import pymysql
from datetime import datetime
from requests.auth import HTTPBasicAuth

URL1CAPI = "http://gw.777-777.org:28880/trade_razrab4/hs/atczak/getdatetimechat/"
URL1CAPIUSER = 'myteam'
URL1CAPIPASS = '777777'

def API1C(phonnuber):
    auth = HTTPBasicAuth(URL1CAPIUSER, URL1CAPIPASS)
    url = URL1CAPI + phonnuber
    #print(url)
    resp = requests.get(url=url, auth=auth)
    content = resp.json()
    return content

def editing_time(time_editer):
    temp = time_editer
    time_editer = f"c {str(datetime.strptime(temp['dateFrom'], '%Y-%m-%dT%H:%M:%S').hour)} до {str(datetime.strptime(temp['dateBy'], '%Y-%m-%dT%H:%M:%S').hour)}"
    return time_editer

def editing_date(date_editer):
    temp = date_editer
    time_editer = []
    for item in temp:
        time_editer.append(f"{str(datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S').day)} {str(mounth(datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S').month))}")
    return time_editer

def mounth(mounth):
        array_mounth = [
            'января',
            'февраля',
            'марта',
            'апреля',
            'мая',
            'июня',
            'июля',
            'августа',
            'сентября',
            'октября',
            'ноября',
            'декабря'
        ]
        return array_mounth[mounth - 1]

def FormButtons(button):
    i = 1
    buttons = "["
    for ItemButtons in button:
            buttons = buttons + "{\"buttonId\": \"" + str(i) + "\", \"buttonText\": \"" + str(ItemButtons) + "\"},"
            i = i + 1
    buttons = buttons[:-1] + "]"
    return buttons

api1c = API1C('9237246968')
button = []
for elem in api1c[1]:
    print("elem: "+str(elem))
    button = []
    if not(elem['date'] in button):
        button.append(elem)
print(button)

print(FormButtons(editing_date(button)))

    #print(editing_time(elem))