from flask import Flask, jsonify, request, abort
import requests
import pymysql
from datetime import datetime
from requests.auth import HTTPBasicAuth
#===========Variables===============


UserDB = 'root'
PassDB = 'BSqr1988ZD'
HostDB = 'localhost'
NameDB = 'whatsapp'
FilePath = "file/"
WebhookURL = "http://31.186.145.79:9001"
URL1CAPI = "http://gw.777-777.org:28880/trade_razrab4/hs/atczak/getdatetimechat/"
URL1CAPIUSER = 'myteam'
URL1CAPIPASS = '777777'

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
                                        "buttons": ''' + buttons + '''
                                    }
                                    '''
        try:
            url = "https://api.green-api.com/waInstance" + self.idInstance + "/SendButtons/" + self.apiTokenInstance
            headers = {'Content-Type': 'application/json'}

            response = requests.request("POST", url, headers=headers, data=payload.encode("UTF-8"))
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
    sql = 'INSERT INTO `whatsapp`.`log` ' \
          '(`timestamp`, `json`) VALUES ' \
          ' (\'' + str(data['timestamp']) + '\',' \
          ' \'' + str(data).replace('\'', '\"') + '\');'
    #print(sql)
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
    sql = "SELECT stage.stage FROM whatsapp.stage where stage.chatid='" + str(data['senderData']['chatId']) + "';"
    # print(sql)
    stage = (database(HostDB, UserDB, PassDB, NameDB, 'read', sql))
    # если клиент выбрал "Повторить заказ"
    api1c = API1C(data['senderData']['chatId'].rstrip('@c.us').replace('7', '', 1))
    if int(stage[0]) == 1:
        # если этап 1
        #print(data['messageData']['typeMessage'])
        if data['messageData']['typeMessage'] == 'buttonsResponseMessage':
            # Если нажата кнопка клиентом
            #print(data['messageData']['buttonsResponseMessage']['selectedButtonId'])
            if int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 1:
                if 'error' in api1c:
                    print(api1c)
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
                    print('Нет ошибок')
            elif int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 2:
                print("Оформляем первый заказ!")
            elif int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 3:
                print("Уузнаем о бонусах")
                WC.SendButton(str(data['senderData']['chatId']), 'Как получить полезные подарки?', buttons=FormButtons(
                    ["Повторить заказ", "Оформить первый заказ", "Перевести в чат с оператором"]),
                              footer='выберите нужный вариант')

    else:
        message = f"На адрес: {str((api1c[0])['address'])}\\nдоставка доступна:\\n"
        button = []
        for elem in api1c[1]:
            print("elem: " + str(elem))
            if not (elem['date'] in button):
                button.append(elem)
        print(button)
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
        print(stage)
        if stage == None:
            #Если первая беседа
            '''message = str(greeting_generator()) +'\\nМеня зовут Ева👩🏼‍💼, я электронный менеджер по приему *заказов воды «Легенда жизни»*\\n' \
                      'Для нашего общения, я подготовила удобное меню\\n' \
                      '👉🏻пришлите, пожалуйста, в ответном сообщении цифру соответствующую выбранному пункту:\\n\\n'
            '''
            message = f'{str(greeting_generator())} \\nМеня зовут Ева👩🏼‍💼, я электронный менеджер по приему *заказов воды «Легенда жизни»*\\n' \
                                        'Для нашего общения, я подготовила удобное меню\\n'
            #print(message)
            WC.SendButton(str(data['senderData']['chatId']), message, buttons=FormButtons(["Повторить заказ", "Оформить первый заказ", "Узнать о бонусах за онлайн заказ"]), footer='выберите нужный вариант')
            sql = "INSERT INTO `whatsapp`.`stage` (`chatid`, `timestamp`, `stage`) VALUES ('" + str(data['senderData']['chatId'] + "', '" + str(data['timestamp'])) + "', '1');"
            #print(sql)
            print(database(HostDB, UserDB, PassDB, NameDB, 'write', sql))
        elif stage == 'rep_stage':
            repeate_order(data)
        else:
            if data['messageData']['typeMessage'] == 'buttonsResponseMessage':
                if int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 1:
                    id = database(HostDB, UserDB, PassDB, NameDB, 'read',
                                  "SELECT id FROM whatsapp.stage where stage.chatid='" + str(
                                      data['senderData']['chatId']) + "';")
                    database(HostDB, UserDB, PassDB, NameDB, 'write',
                             "UPDATE `whatsapp`.`stage` SET `stage_type` = 'rep_stage' WHERE(`id` = '" + str(id[0]) + "') and (`chatid` = '" + str(data['senderData']['chatId']) + "');")
                    repeate_order(data)
                elif int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 2:
                    print("Оформляем первый заказ!")
                elif int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 3:
                    print("Узнаем о бонусах")
                    WC.SendButton(str(data['senderData']['chatId']), 'Как получить полезные подарки?', buttons=FormButtons(
                        ["Повторить заказ", "Оформить первый заказ", "Перевести в чат с оператором"]),
                                  footer='выберите нужный вариант')
            else:
                print("Не правильный ответ")

    else:
        return 200
    pass
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

@app.route('/', methods=['POST'])
def hello():
    #print(request.json)
    logingdata(request.json)
    gateway(request.json)
    return '200'
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9001)
