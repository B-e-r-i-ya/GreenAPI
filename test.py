from flask import Flask, jsonify, request, abort
import requests
import pymysql
from datetime import datetime
from requests.auth import HTTPBasicAuth

UserDB = 'root'
PassDB = 'BSqr1988ZD'
HostDB = 'localhost'
NameDB = 'whatsapp'
FilePath = "file/"
WebhookURL = "http://31.186.145.79:9001"
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

def database(HostDB, UserDB, PassDB, NameDB, type, sql):
    '''

    :param HostDB:
    :param UserDB:
    :param PassDB:
    :param NameDB:
    :param type: тип запроса к базе read = чтение(select)
    :param sql:
    :return:
    '''
    try:
        cnx = pymysql.connect(user=UserDB, password=PassDB,
                                         host=HostDB,
                                         database=NameDB)
        with cnx:
            cursor = cnx.cursor()
            if type == 'write':
                cursor.execute(sql)
                cnx.commit()
            elif type == 'read':
                cur = cnx.cursor()
                cur.execute(sql)
                #result = cur.fetchone()
                #for x in result:
                #    print(x)
                return cur.fetchone()
    except pymysql.Error as err:
        #print(err)
        return err


'''api1c = API1C('9237246968')
button = []
for elem in api1c[1]:
    print("elem: "+str(elem))
    button = []
    if not(elem['date'] in button):
        button.append(elem)'''
#print(button)

#print(FormButtons(editing_date(button)))

    #print(editing_time(elem))

'''api = [ { "address": "г Новоалтайск, ул Белоярская, Дом 212, " }, [{ "date": "2022-10-19T00:00:00", "dateFrom": "2022-10-19T13:01:00", "dateBy": "2022-10-19T17:00:00" } ], [ { "nomenclature": "Вода питьевая\"Легенда жизни\" 19л", "quantity": 2, "price": 440, "form_of_payment": "Наличная" } ], { "kodpartner": "Б000104759 " } ]

print(api[1][0]['date'])

button = []
for elem in api[1]:
    print("elem: "+str(elem))
    button = []
    if not(elem['date'] in button):
        button.append(elem)


print(button)
print(editing_date(button))'''


def mounth(mounth):
    if type(mounth) == int:
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

    elif type(mounth) == str:
        array_mounth = {
            'января': "1",
            'февраля': "2",
            'марта': "3",
            'апреля': "4",
            'мая': "5",
            'июня': "6",
            'июля': "7",
            'августа': "8",
            'сентября': "9",
            'октября': "10",
            'ноября': "11",
            'декабря': "12"
            }
        return array_mounth[mounth]

#now = datetime.today()
#print(datetime.today().year)
#date = "31 октября"

#print(date.split()[0])
#print(mounth(date.split()[1]))
api1c = [ { "address": "г Барнаул, пр-кт Энергетиков, Дом 4, " }, [ { "date": "2022-10-31T00:00:00", "dateFrom": "2022-10-31T11:01:00", "dateBy": "2022-10-31T13:00:00" }, { "date": "2022-10-31T00:00:00", "dateFrom": "2022-10-31T15:01:00", "dateBy": "2022-10-31T17:00:00" }, { "date": "2022-10-31T00:00:00", "dateFrom": "2022-10-31T17:01:00", "dateBy": "2022-10-31T19:00:00" }, { "date": "2022-10-31T00:00:00", "dateFrom": "2022-10-31T19:01:00", "dateBy": "2022-10-31T21:00:00" } ], [ { "nomenclature": "Вода питьевая\"Легенда жизни\" 19л", "quantity": 2, "price": 440, "form_of_payment": "Наличная" } ], { "kodpartner": "Б000104759 " } ]
#print(database(HostDB, UserDB, PassDB, NameDB, 'write', f"INSERT INTO `whatsapp`.`new_order` (`chatid`, `date`, `datefrom`, `dateBy`, `kodpartner`) VALUES ('{str(data['senderData']['chatId'])}', '{str(date)}', '', '', {str(api1c[3]['kodpartner'])}';"))

def quantity_bootle(quantity):
    if int(quantity) == 1:
        return "бутыль"
    elif int(quantity) in [2,3,4]:
        return "бутыли"
    else:
        return "бутылей"
message = "В прошлый раз Вы заказывали: \n"
for item in api1c[2]
    message = message + item['nomenclature'] + " " + str(item['quantity']) + " " +quantity_bootle(item['quantity'])

print(message)