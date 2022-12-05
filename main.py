from flask import Flask, jsonify, request, abort
import requests
import time
import pymysql
from datetime import datetime
from requests.auth import HTTPBasicAuth
from threading import Thread
#===========Variables===============


UserDB = ''
PassDB = ''
HostDB = 'localhost'
NameDB = 'whatsapp'
FilePath = "file/"
WebhookURL = ""
URL1CAPI = ""
URL1CAPIUSER = ''
URL1CAPIPASS = ''

class GreenAPI():
    idInstance = ''
    apiTokenInstance = ''
    def __init__(self, idInstance, apiTokenInstance, webhookInstance=None):
        self.idInstance = idInstance
        self.apiTokenInstance = apiTokenInstance
        if webhookInstance != None:
            try:
                url = "https://api.green-api.com/waInstance" + str(idInstance) + "/setSettings/" + str(apiTokenInstance)

                payload = "{" \
                          "\r\n\t\"countryInstance\": \"ru\"," \
                          "\r\n\t\"webhookUrl\": \"" + webhookInstance + "\"," \
                          "\r\n\t\"delaySendMessagesMilliseconds\": 1000," \
                          "\r\n\t\"markIncomingMessagesReaded\": \"yes\"," \
                          "\r\n\t\"outgoingWebhook\": \"yes\"," \
                          "\r\n\t\"stateWebhook\": \"yes\"," \
                          "\r\n\t\"incomingWebhook\": \"yes\"," \
                          "\r\n\t\"deviceWebhook\": \"yes\"\r\n" \
                          "}"
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
            except requests.ConnectionError as e:
                print(e)

    def reloadInstans(self):
        try:
            url = "https://api.green-api.com/waInstance" + self.idInstance + "/reboot/" + self.apiTokenInstance

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            return response
        except requests.ConnectionError as e:
            print(e)

    def receiveQRcode(self):
        try:
            url = "https://api.green-api.com/waInstance" + self.idInstance + "/qr/" + self.apiTokenInstance

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            return response
        except requests.ConnectionError as e:
            print(e)


    def SendMessage(self, chatId, message):
        try:
            url = "https://api.green-api.com/waInstance" + self.idInstance + "/sendMessage/" + self.apiTokenInstance

            payload = "{\r\n\t\"chatId\": \"" + chatId + "\",\r\n\t\"message\": \"" + message + "\"\r\n}"
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload.encode("UTF-8"))
            return response
        except requests.ConnectionError as e:
            print(e)
    def SendButton(self, chatId, message, buttons, footer=None):
        if footer == None:
            payload = '''{
                                        "chatId": "''' + str(chatId) + '''",
                                        "message": "''' + str(message) + '''",
                                        "buttons": ''' + str(buttons) + '''
                                    }
                                    '''
        else:
            payload = '''{
                                        "chatId": "''' + str(chatId) + '''",
                                        "message": "''' + str(message) + '''",
                                        "footer": "''' + str(footer) + '''",
                                        "buttons": ''' + str(buttons) + '''
                                    }
                                    '''
        try:
            url = "https://api.green-api.com/waInstance" + self.idInstance + "/SendButtons/" + self.apiTokenInstance
            headers = {'Content-Type': 'application/json'}

            response = requests.request("POST", url, headers=headers, data=payload.encode("UTF-8"))
            print(payload)
            print(response.json())
            return response
        except requests.ConnectionError as e:
            print(e)

    def SendTemplateButton(self, chatId, message, buttons, footer=None):
        if footer == None:
            payload = '''{
                                        "chatId": "''' + str(chatId) + '''",
                                        "message": "''' + str(message) + '''",
                                        "templateButtons": ''' + buttons + '''
                                    }
                                    '''
        else:
            payload = '''{
                                        "chatId": "''' + str(chatId) + '''",
                                        "message": "''' + str(message) + '''",
                                        "footer": "''' + str(footer) + '''",
                                        "templateButtons": ''' + buttons + '''
                                    }
                                    '''
        try:
            url = "https://api.green-api.com/waInstance" + str(self.idInstance) + "/SendButtons/" + str(
                self.apiTokenInstance) + ""

            print(payload)
            headers = {'Content-Type': 'application/json'}

            response = requests.request("POST", url, headers=headers, data=payload.encode("UTF-8"))
            return response
        except requests.ConnectionError as e:
            print(e)

def editing_time(time_editer):
    temp = time_editer
    time_editer = f"c {str(datetime.strptime(temp['dateFrom'], '%Y-%m-%dT%H:%M:%S').hour)} до {str(datetime.strptime(temp['dateBy'], '%Y-%m-%dT%H:%M:%S').hour)}"
    return time_editer

def editing_date(date_editer):
    temp = date_editer
    date_editer = []
    for item in temp:
        date_editer.append(f"{str(datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S').day)} {str(mounth(datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S').month))}")
    print(date_editer)
    return date_editer

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

buttons = ["Привет", "Пока"]
def FormButtons(button):
    i = 1
    buttons = "["
    for ItemButtons in button:
            buttons = buttons + "{\"buttonId\": \"" + str(i) + "\", \"buttonText\": \"" + str(ItemButtons) + "\"},"
            i = i + 1
    buttons = buttons[:-1] + "]"
    return buttons

def FormTemplateButtons(templatebutton):
    i = 1
    buttons = "["
    for ItemButtons in templatebutton:
        buttons = buttons + "{\"index\": \"" + str(i) + "\", \"buttonText\": \"" + str(ItemButtons) + "\"},"
        i = i + 1
    buttons = buttons[:-1] + "]"
    return buttons

def logingdata(data):
    '''

    :param data: json ответ от API
    :return:
    '''
    print("Loging: ")
    sql = 'INSERT INTO `whatsapp`.`log` ' \
          '(`timestamp`, `json`) VALUES ' \
          ' (\'' + str(data['timestamp']) + '\',' \
          ' \'' + str(data).replace('\'', '\"') + '\');'
    print(sql)
    database(HostDB, UserDB, PassDB, NameDB, 'write', sql)
    #print(data)
    #database(HostDB, UserDB, PassDB, NameDB, 'write', "DELETE FROM `whatsapp`.`stage` WHERE timestamp < (CURDATE() - INTERVAL 1 MINUTE);")
    #print("data =" + str(data))
    if data['typeWebhook'] == 'stateInstanceChanged':
        return 200
    elif data['typeWebhook'] == 'incomingMessageReceived':
        '''если входящее сообщение. Записываем данные в базу'''
        sql = 'INSERT INTO `whatsapp`.`messages` ' \
              '(`id_message`, `timestamp`, `sender_chatid`, `sender_name`, `type_message`) VALUES ' \
              '(\'' + str(data['idMessage']) + '\',' \
              ' \'' + str(data['timestamp']) + '\',' \
              ' \'' + str(data['senderData']['chatId']) + '\',' \
              ' \'' + str(data['senderData']['senderName']) + '\',' \
              ' \'' + str(data['messageData']['typeMessage']) + '\');'
        database(HostDB, UserDB, PassDB, NameDB, 'write', sql)
        if data['messageData']['typeMessage'] == 'textMessage':
            '''
            если входящее сообщение и тип сообщения textMessage
            '''
            sql = 'INSERT INTO `whatsapp`.`text_message` ' \
                  '(`id_message`, `text_message`) VALUES ' \
                  '(\'' + str(data['idMessage']) + '\',' \
                  ' \'' + str(data['messageData']['textMessageData']['textMessage']) + '\');'
            database(HostDB, UserDB, PassDB, NameDB, 'write', sql)
        elif data['messageData']['typeMessage'] == 'extendedTextMessage':
            '''
            если входящее сообщение и тип сообщения extendedTextMessage
            '''
            sql = 'INSERT INTO `whatsapp`.`text_message` ' \
                  '(`id_message`, `text_message`) VALUES ' \
                  '(\'' + str(data['idMessage']) + '\',' \
                                                   ' \'' + str(
                data['messageData']['textMessageData']['textMessage']) + '\');'
        elif data['messageData']['typeMessage'] in ["imageMessage", "videoMessage", "documentMessage", "audioMessage"]:
            '''
            если входящее сообщение и тип сообщения "imageMessage", "videoMessage", "documentMessage", "audioMessage"
            '''
            path = FilePath + data['messageData']['fileMessageData']['fileName']

            #Извлекаем медиафайл и сохраняем в файл
            with open(path, 'wb') as f:
                f.write(requests.get(data['messageData']['fileMessageData']['downloadUrl']).content)
            #Записываем данные в базу
            sql = 'INSERT INTO `whatsapp`.`mediaMessage` ' \
                  '(`id_message`, `downloadUrl`, `caption`, `path`) VALUES ' \
                  '(\'' + str(data['idMessage']) + '\',' \
                  ' \'' + str(data['messageData']['fileMessageData']['downloadUrl']) + '\',' \
                  ' \'' + str(data['messageData']['fileMessageData']['caption']) + '\',' \
                  ' \'' + path + '\');'
            database(HostDB, UserDB, PassDB, NameDB, 'write', sql)
        elif data['messageData']['typeMessage'] == 'buttonsResponseMessage':
            '''
            если входящее сообщение и тип сообщения buttonsResponseMessage
            '''
            sql = 'INSERT INTO `whatsapp`.`buttonsResponseMessage` ' \
                  '(`id_message`, `stanzaId`, `selectedButtonId`, `selectedButtonText`) VALUES ' \
                  '(\'' + str(data['idMessage']) + '\',' \
                  ' \'' + str(data['messageData']['buttonsResponseMessage']['stanzaId']) + '\',' \
                  ' \'' + str(data['messageData']['buttonsResponseMessage']['selectedButtonId']) + '\',' \
                  ' \'' + str(data['messageData']['buttonsResponseMessage']['selectedButtonText']) + '\');'
            database(HostDB, UserDB, PassDB, NameDB, 'write', sql)
        else:
            # Все что не обработали

            return 200
        print(database(HostDB, UserDB, PassDB, NameDB, 'write', sql))
    else:
        # Все что не обработали
        return 200

def API1C(phonnuber):
    auth = HTTPBasicAuth(URL1CAPIUSER, URL1CAPIPASS)
    url = URL1CAPI + phonnuber
    #print(url)
    resp = requests.get(url=url, auth=auth)
    content = resp.json()
    #print(content)
    return content

def greeting_generator():
    if 5 <= int(datetime.now().hour) <= 10:
        greeting = "Доброе утро!"
    elif 11 <= int(datetime.now().hour) <= 17:
        greeting = "Добрый день!"
    elif 18 <= int(datetime.now().hour) <= 21:
        greeting = "Добрый вечер!"
    elif 22 <= int(datetime.now().hour) <= 23 or 0 <= int(datetime.now().hour) <= 4:
        greeting = "Доброй ночи!"
    return greeting

def quantity_bootle(quantity):
    if int(quantity) == 1:
        return "бутыль"
    elif int(quantity) in [2,3,4]:
        return "бутыли"
    else:
        return "бутылей"

def dbmigrate():
    from os import path
    try:
        cnx = pymysql.connect(user=UserDB, password=PassDB,
                                         host=HostDB,
                                         database=NameDB)
        with cnx:
            cursor = cnx.cursor()
            cursor.execute("show databases;")
            cnx.commit()
    except pymysql.Error as err:
        print(err)
        if str(err) == '(1049, "Unknown database \'whatsapp\'")':
            print("Базы нет! Запускаю миграцию!")

            # File did not exists
            if path.isfile("db.sql") is False:
                print("File load error : {}".format("db.sql"))
                return False

            else:
                with open("db.sql", "r") as sql_file:
                    # Split file in list
                    ret = sql_file.read().split(';')
                    # drop last empty entry
                    ret.pop()

            if ret is not False:
                for sql_item in ret:
                    print(sql_item)
                    print(database(HostDB, UserDB, PassDB, NameDB=None, type="write", sql=sql_item))
        else:
            print(err)

def repeate_order(data):
    print('repeate_order')
    sql = "SELECT stage.stage FROM whatsapp.stage where stage.chatid='" + str(data['senderData']['chatId']) + "';"
    # print(sql)
    stage = (database(HostDB, UserDB, PassDB, NameDB, 'read', sql))
    # если клиент выбрал "Повторить заказ"
    api1c = API1C(data['senderData']['chatId'].rstrip('@c.us').replace('7', '', 1))
    if int(stage[0]) == 0:
        print("stage0")
        print(data['messageData']['typeMessage'])
        if data['messageData']['typeMessage'] == 'buttonsResponseMessage':
            if data['messageData']['buttonsResponseMessage']['selectedButtonText'] == 'да':
                id = database(HostDB, UserDB, PassDB, NameDB, 'read',
                              f"SELECT id FROM whatsapp.stage where stage.chatid='{str(data['senderData']['chatId'])}';")
                database(HostDB, UserDB, PassDB, NameDB, 'write',
                         f"UPDATE `whatsapp`.`stage` SET `stage` = '1' WHERE(`id` = '{str(id[0])}') and (`chatid` = '{str(data['senderData']['chatId'])}');")
                repeate_order(data)
            elif data['messageData']['buttonsResponseMessage']['selectedButtonText'] == 'нет':
                WC.SendButton(data['senderData']['chatId'], "Правильно! \\n Зачем повторять!", FormButtons(["Повторить заказ","Оформить первый заказ","Узнать о бонусах за онлайн заказ","Перевести в чат с оператором"]))
            elif data['messageData']['buttonsResponseMessage']['selectedButtonText'] == 'Повторить заказ':
                print("не кнопка")
                message = "В прошлый раз Вы заказывали: \\n"
                for item in api1c[2]:
                    message = message + str(item['nomenclature']).replace('\"', '\\"') + " " + str(item['quantity']) + " " + quantity_bootle(
                        item['quantity'])
                message = message + "\\n Повторим заказ?"
                print(WC.SendButton(data['senderData']['chatId'], message, FormButtons(['да', 'нет'])))
    elif int(stage[0]) == 1:
        # если этап 1
        #print(data['messageData']['typeMessage'])
        if data['messageData']['typeMessage'] == 'buttonsResponseMessage':
            # Если нажата кнопка клиентом
            #print(data['messageData']['buttonsResponseMessage'])
            if data['messageData']['buttonsResponseMessage']['selectedButtonText'] == 'да':
                if 'error' in api1c:
                    message = api1c['error']
                    if message in ["Нет партнера с таким номером телефона", "Более одного партнера с главным номером",
                                   "Партнер не является физическим лицом", "Нет адреса доставки подходящего критериям",
                                   "Более одного адреса доставки", "В адресе доставки не указана зона доставки"]:
                        print(message)
                        WC.SendMessage(data['senderData']['chatId'],
                                       "К сожалению, Ваш номер не привязан к функции «Повторить заказ».\\n"
                                       "Привязать его можно прямо сейчас. Это займёт всего 2 минуты.\\n"
                                       "Напишите данные, которые Вы используете при заказе воды:\\n"
                                       "- Фамилия, имя, отчество / Наименование организации\\n"
                                       "- Адрес доставки\\n")
                    elif message in ["У партнера есть заказ на вчера, сегодня, завтра",
                                     "У партнера последний заказ не соответствующий критериям",
                                     "У партнера в последнем заказе есть товар не соответствующий критериям"]:
                        WC.SendMessage(data['senderData']['chatId'],
                                       "К сожалению, Ваш последний заказ не подходит по параметрам для автоматического повторения.\\n"
                                       "Оставайтесь в диалоге, оператор подключиться к Вам в течение  2 минут.\\n"
                                       "Чтобы не ждать ответа оператора оформите свой заказ на сайте прямо сейчас:\\n"
                                       " https://777-777.org\\n")
                else:
                    #print(api1c)
                    print('Нет ошибок')
                    if api1c[1] == []:
                        WC.SendButton(data['senderData']['chatId'], "К сожалению доставка по вашему адресу на бижайшии дни не доступна!", buttons=FormButtons(
                    ["Оформить первый заказ", "Узнать о бонусах за онлайн-заказы","Перевести в чат с оператором"]))

                    else:
                        address = api1c[0]['address']
                        button = []
                        for elem in api1c[1]:
                            print(f"{str(datetime.strptime(elem['date'], '%Y-%m-%dT%H:%M:%S').day)} {str(mounth(datetime.strptime(elem['date'], '%Y-%m-%dT%H:%M:%S').month))}")
                            temp_elem = f"{str(datetime.strptime(elem['date'], '%Y-%m-%dT%H:%M:%S').day)} {str(mounth(datetime.strptime(elem['date'], '%Y-%m-%dT%H:%M:%S').month))}"
                            if not (temp_elem in button):
                                button.append(temp_elem)
                            else:
                                print("Элемент есть!")

                        print(button)
                        #WC.SendButton(data['senderData']['chatId'], f'Мы уже готовы доставить "Легенду" по адресу { str(address) } .', FormButtons(button), footer='Просто выберите дату:')
                        WC.SendButton(data['senderData']['chatId'],
                                      f"Мы уже готовы доставить 'Легенду' по адресу {str(address)} .",
                                      FormButtons(button), footer='Просто выберите дату:')
                        id = database(HostDB, UserDB, PassDB, NameDB, 'read',
                                      "SELECT id FROM whatsapp.stage where stage.chatid='" + str(
                                          data['senderData']['chatId']) + "';")
                        database(HostDB, UserDB, PassDB, NameDB, 'write',
                                 "UPDATE `whatsapp`.`stage` SET `stage` = '2' WHERE(`id` = '" + str(
                                     id[0]) + "') and (`chatid` = '" + str(data['senderData']['chatId']) + "');")
            elif data['messageData']['buttonsResponseMessage']['selectedButtonText'] == 'Оформляем первый заказ!':
                print("Оформляем первый заказ!")
            elif data['messageData']['buttonsResponseMessage']['selectedButtonText'] == 'Узнать о бонусах за онлайн-заказ':
                print("Узнаем о бонусах")
                WC.SendButton(str(data['senderData']['chatId']), 'Как получить полезные подарки?', buttons=FormButtons(
                    ["Повторить заказ", "Оформить первый заказ", "Перевести в чат с оператором"]),
                              footer='выберите нужный вариант')
    elif int(stage[0]) == 2:
        print("!!!!stage 2!!!!!")
        if data['messageData']['typeMessage'] == 'buttonsResponseMessage':
            date = data['messageData']['buttonsResponseMessage']['selectedButtonText']
            date = date.split()
            id = database(HostDB, UserDB, PassDB, NameDB, 'read',f"SELECT id FROM whatsapp.stage where stage.chatid='{str(data['senderData']['chatId'])}';")
            date = f"{str(datetime.today().year)}-{str(mounth(date[1]))}-{str(date[0])}T00:00:00"
            sql = f"INSERT INTO `whatsapp`.`new_order` (`chatid`, `date`, `datefrom`, `dateBy`, `kodpartner`, `order_placed`) VALUES ('{str(data['senderData']['chatId'])}', '{str(date)}', '', '', '{str(api1c[3]['kodpartner'])}', False);"
            print(sql)
            print(database(HostDB, UserDB, PassDB, NameDB, 'write', sql))
            time = []
            for item in api1c[1]:
                #print("item: " + str(item['date']))
                #print(f'date: {str(date)}')
                if str(item['date']) == str(date):
                    print("time: " + str(editing_time(item)))
                    time.append(editing_time(item))

            WC.SendButton(data['senderData']['chatId'],
                          f"Какое время будет удобно?",
                          FormButtons(time), footer='Просто выберите время:')
            database(HostDB, UserDB, PassDB, NameDB, 'write', f"UPDATE `whatsapp`.`stage` SET `stage` = '3' WHERE(`id` = '{str(id[0])}') and (`chatid` = '{str(data['senderData']['chatId'])}');")
    elif int(stage[0]) == 3:
        print("!!!!stage 3!!!!!")
        time = str(data['messageData']['buttonsResponseMessage']['selectedButtonText']).split()
        id_stage = database(HostDB, UserDB, PassDB, NameDB, 'read',f"SELECT id FROM whatsapp.stage where stage.chatid='{str(data['senderData']['chatId'])}';")[0]
        id_new_order = database(HostDB, UserDB, PassDB, NameDB, 'read',f"SELECT id FROM whatsapp.new_order where new_order.chatid='{str(data['senderData']['chatId'])}';")[0]
        print(id_new_order)
        date = database(HostDB, UserDB, PassDB, NameDB, 'read',f"SELECT date FROM whatsapp.new_order where new_order.chatid='{str(data['senderData']['chatId'])}';")
        if database(HostDB, UserDB, PassDB, NameDB, 'write',f"UPDATE `whatsapp`.`new_order` SET `datefrom` = '{str(date[0]).partition('T')[0]}T{time[1]}:00:00', `dateBy` = '{str(date[0]).partition('T')[0]}T{time[3]}:00:00' WHERE (`id` = '{id_new_order}');") == None:
            print("Оформляем заказ!!!")
            WC.SendMessage(str(data['senderData']['chatId']), "Заказ оформлен")
            database(HostDB, UserDB, PassDB, NameDB, 'write',
                     f"UPDATE `whatsapp`.`new_order` SET `order_placed` = True WHERE (`id` = '{id_new_order}');")
            database(HostDB, UserDB, PassDB, NameDB, 'write', f"DELETE FROM `whatsapp`.`stage` WHERE (`id` = '{id_stage}');")
    else:
        message = f"На адрес: {str((api1c[0])['address'])}\\nдоставка доступна:\\n"
        button = []
        for elem in api1c[1]:
            print("elem!!!!: " + str(elem))
            print("Что за хуйня!!!")
            if not (elem['date'] in button):
                button.append(elem)
            else:
                print(elem['date'])
        print("кнопка" + str(editing_date(button)))
        WC.SendButton(str(data['senderData']['chatId']), message, FormButtons(editing_date(button)))
        id = database(HostDB, UserDB, PassDB, NameDB, 'read',
                      "SELECT id FROM whatsapp.stage where stage.chatid='" + str(
                          data['senderData']['chatId']) + "';")
        database(HostDB, UserDB, PassDB, NameDB, 'write',
                 "UPDATE `whatsapp`.`stage` SET `stage` = '2' WHERE(`id` = '" + str(id[
                     0]) + "') and (`chatid` = '" + str(data['senderData']['chatId']) + "');")
        '''WC.SendButton(str(data['senderData']['chatId']),
                      '',
                      buttons=FormButtons(
                          ["Повторить заказ", "Оформить первый заказ", "Перевести в чат с оператором"]),
                      footer='выберите нужный вариант')'''

def error(data):
    sql = "SELECT stage_error.stage FROM whatsapp.stage_error where stage_error.chatid='" + str(data['senderData']['chatId']) + "';"
    print(sql)
    err = (database(HostDB, UserDB, PassDB, NameDB, 'read', sql))
    if err == None or int(err[0]) < 3:
            WC.SendMessage(str(data['senderData']['chatId']), "Извините не понятно!")
            if err == None:
                sql = "INSERT INTO `whatsapp`.`stage_error` (`chatid`, `timestamp`, `stage`) VALUES ('" + str(
                    data['senderData']['chatId'] + "', '" + str(data['timestamp'])) + "', '1');"
                # print(sql)
                print(database(HostDB, UserDB, PassDB, NameDB, 'write', sql))
            else:
                err_temp = int(err[0])+1
                id = database(HostDB, UserDB, PassDB, NameDB, 'read',
                              "SELECT id FROM whatsapp.stage_error where stage_error.chatid='" + str(
                                  data['senderData']['chatId']) + "';")
                database(HostDB, UserDB, PassDB, NameDB, 'write',
                         "UPDATE `whatsapp`.`stage_error` SET `stage` = '" + str(err_temp) + "' WHERE(`id` = '" + str(id[
                             0]) + "') and (`chatid` = '" + str(data['senderData']['chatId']) + "');")
    else:
        print("вызываем оператора")

def gateway(data):
    if data['typeWebhook'] == 'incomingMessageReceived':
        #print(data['senderData']['chatId'])
        sql = "SELECT stage.stage_type FROM whatsapp.stage where stage.chatid='" + str(data['senderData']['chatId']) + "';"
        #print(sql)
        stage = (database(HostDB, UserDB, PassDB, NameDB, 'read', sql))
        print("stage:" + str(stage))
        #if data['messageData']['typeMessage'] == 'buttonsResponseMessage':
        #    print(data['messageData']['buttonsResponseMessage'])
        if stage == None:
            #Если первая беседа
            '''message = str(greeting_generator()) +'\\nМеня зовут Ева👩🏼‍💼, я электронный менеджер по приему *заказов воды «Легенда жизни»*\\n' \
                      'Для нашего общения, я подготовила удобное меню\\n' \
                      '👉🏻пришлите, пожалуйста, в ответном сообщении цифру соответствующую выбранному пункту:\\n\\n'
            '''
            message = f'{str(greeting_generator())} \\nМеня зовут Ева👩🏼‍💼, я электронный менеджер по приему *заказов воды «Легенда жизни»*\\n' \
                                        'Для нашего общения, я подготовила удобное меню\\n'
            #print(message)
            WC.SendButton(str(data['senderData']['chatId']), message, buttons=FormButtons(['Повторить заказ', 'Оформить первый заказ', 'Узнать о бонусах за онлайн заказ']), footer='выберите нужный вариант')
            sql = "INSERT INTO `whatsapp`.`stage` (`chatid`, `timestamp`, `stage`) VALUES ('" + str(data['senderData']['chatId'] + "', '" + str(data['timestamp'])) + "', '0');"
            #print(sql)
            database(HostDB, UserDB, PassDB, NameDB, 'write', sql)

        elif data['messageData']['typeMessage'] == 'buttonsResponseMessage' and str(data['messageData']['buttonsResponseMessage']['selectedButtonText']) == 'Повторить заказ':
            id = database(HostDB, UserDB, PassDB, NameDB, 'read',
                          "SELECT id FROM whatsapp.stage where stage.chatid='" + str(
                              data['senderData']['chatId']) + "';")
            database(HostDB, UserDB, PassDB, NameDB, 'write',
                     "UPDATE `whatsapp`.`stage` SET `stage_type` = 'rep_stage' WHERE(`id` = '" + str(id[0]) + "') and (`chatid` = '" + str(data['senderData']['chatId']) + "');")
            repeate_order(data)
            return 200
        elif data['messageData']['typeMessage'] == 'buttonsResponseMessage' and str(data['messageData']['buttonsResponseMessage']['selectedButtonText']) == 'Оформить первый заказ':
            print("Оформляем первый заказ!")
            return 200
        elif data['messageData']['typeMessage'] == 'buttonsResponseMessage' and str(data['messageData']['buttonsResponseMessage']['selectedButtonText']) == 'Узнать о бонусах за онлайн заказ':
            print("Узнаем о бонусах")
            WC.SendButton(str(data['senderData']['chatId']), 'Как получить полезные подарки?', buttons=FormButtons(
                ["Повторить заказ", "Оформить первый заказ", "Перевести в чат с оператором"]),
                          footer='выберите нужный вариант')
            return 200

        elif data['messageData']['typeMessage'] == 'buttonsResponseMessage' and 'rep_stage' in stage:
            repeate_order(data)
        else:
            print("Не правильный ответ")
            return 200

    else:
        return 200
#rint(str(FormButtons(buttons)))

dbmigrate()
WC = GreenAPI("1101754804", "d660db8008434810a96c21062cd770d2e24ed3415d534f9fae", webhookInstance=WebhookURL)

#test = WC.SendButton(chatId="79237246968@c.us", message="Херня", buttons=FormButtons(buttons), footer="Нажми")
#print(test.text.encode('utf8'))


'''try:
    con = pymysql.connect(user=UserDB, password=PassDB,
                          host=HostDB,
                          database=NameDB)
    con.close()
except pymysql.Error as err:
    print(type(err))
    if str(err) == "(1049, \"Unknown database 'whatsapp'\")":
        con = pymysql.connect(user=UserDB, password=PassDB,
                              host=HostDB)
        with open("db.sql") as file:
            sql = file.read()
            print(sql)
        with con:
            cursor = con.cursor()
            if type == 'write':
                cursor.execute(sql)
                con.commit()'''

app = Flask(__name__)

class Compute(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def run(self):
        logingdata(self.request.json)
        gateway(self.request.json)

@app.route('/', methods=['POST'])
def hello():
    #print(request.json)
    thread_a = Compute(request.__copy__())
    thread_a.start()
    return '200'
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9001)
    logingdata(request.json)
    gateway(request.json)
