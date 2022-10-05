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

            response = requests.request("POST", url, headers=headers, data=payload)
            return response
        except requests.ConnectionError as e:
            print(e)
    def SendButton(self, chatId, message, buttons, footer=None):
        if footer == None:
            payload = '''{
                                        "chatId": "''' + str(chatId) + '''",
                                        "message": "''' + str(message) + '''",
                                        "buttons": ''' + buttons + '''
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
    temp = time_editer.split()
    time_editer = "c " + str(datetime.strptime(temp[0], '%Y-%m-%dT%H:%M:%S').hour) + " до " + str(
        datetime.strptime(temp[1], '%Y-%m-%dT%H:%M:%S').hour)
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
                return cur.fetchone()
    except pymysql.Error as err:
        print(err)
        cnx.close()

buttons = ["Привет", "Пока"]
def FormButtons(button):
    i = 1
    buttons = "["
    for ItemButtons in button:
            buttons = buttons + "{\"buttonId\": \"" + str(i) + "\", \"buttonText\": \"" + str(ItemButtons) + "\"},"
            i = i + 1
    buttons = buttons[:-1] + "]"
    return buttons

'''
{
    "chatId": "79001234567@c.us",
    "message": "Hello",
    "footer": "What kind of action will you choose?",
    "templateButtons": [
            {"index": 1, "urlButton": {"displayText": "⭐ Star us on GitHub!", "url": "https://github.com/green-api/docs"}},
            {"index": 2, "callButton": {"displayText": "Call us", "phoneNumber": "+1 (234) 5678-901"}},
            {"index": 3, "quickReplyButton": {"displayText": "Plain button", "id": "plainButtonId"}}
        ]
}
'''

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
        print(database(HostDB, UserDB, PassDB, NameDB, 'read', sql))
    else:
        # Все что не обработали
        return 200

def API1C(phonnuber):
    auth = HTTPBasicAuth(URL1CAPIUSER, URL1CAPIPASS)
    url = URL1CAPI + phonnuber
    resp = requests.get(url=url, auth=auth)
    content = resp.json()
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

def gateway(data):
    if data['typeWebhook'] == 'incomingMessageReceived':
        #print(data['senderData']['chatId'])
        sql = "SELECT stage.stage FROM whatsapp.stage where stage.chatid='" + str(data['senderData']['chatId']) + "';"
        stage = (database(HostDB, UserDB, PassDB, NameDB, 'read', sql))
        print(stage)
        if stage == None:
            #Если первая беседа
            message = str(greeting_generator()) +'\\nМеня зовут Ева👩🏼‍💼, я электронный менеджер по приему *заказов воды «Легенда жизни»*\\n' \
                      'Для нашего общения, я подготовила удобное меню\\n' \
                      '👉🏻пришлите, пожалуйста, в ответном сообщении цифру соответствующую выбранному пункту:\\n\\n'
            #print(message)
            WC.SendButton(str(data['senderData']['chatId']), message, buttons=FormButtons(["Повторить заказ", "Оформить первый заказ", "Узнать о бонусах за онлайн заказ"]), footer='выберите нужный вариант')
            database(HostDB, UserDB, PassDB, NameDB, 'write', "INSERT INTO `whatsapp`.`stage` (`chatid`, `timestamp`, `stage`) VALUES ('" + str(data['senderData']['chatId'] + "', '" + str(data['timestamp'])) + "', '1');")
        elif int(stage[0]) == 1:
            #если этап 1
            #print(data)
            if data['messageData']['typeMessage'] == 'buttonsResponseMessage':
                #Если нажата кнопка клиентом
                #print(type(data['messageData']['buttonsResponseMessage']['selectedButtonId']))
                if int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 1:
                    #если клиент выбрал "Повторить заказ"
                    api1c = API1C(data['senderData']['chatId'].rstrip('@c.us'))
                    if 'error' in api1c:
                        print(api1c['error'])
                        message = api1c['error']
                        if message in ["Нет партнера с таким номером телефона", "Более одного партнера с главным номером", "Партнер не является физическим лицом", "Нет адреса доставки подходящего критериям", "Более одного адреса доставки", "В адресе доставки не указана зона доставки"]:
                            print(message)
                            pass
                        elif message in ["У партнера есть заказ на вчера, сегодня, завтра",
                                               "У партнера последний заказ не соответствующий критериям",
                                               "У партнера в последнем заказе есть товар не соответствующий критериям"]:
                            pass
                    else:
                        message = "На адрес: " + str((api1c.json()[0])['address']) + "\\n" + "доставка доступна:\\n"
                        button = []
                        for elem in api1c.json()[1]:
                            '''button.append(str((datetime.strptime(elem['date'], '%Y-%m-%dT%H:%M:%S')).strftime('%Y.%m.%d')) + " с " + str((datetime.strptime(elem['dateFrom'], '%Y-%m-%dT%H:%M:%S')).strftime(
                                    '%H:%M')) + " до " + str((datetime.strptime(elem['dateBy'], '%Y-%m-%dT%H:%M:%S')).strftime('%H:%M')))'''
                            button.append(editing_time(elem))
                        print(message)
                        print(button)
                        WC.SendButton(str(data['senderData']['chatId']), message, button)
                        id = database(HostDB, UserDB, PassDB, NameDB, 'read', "SELECT id FROM whatsapp.stage where stage.chatid='" + str(data['senderData']['chatId']) + "';")
                        database(HostDB, UserDB, PassDB, NameDB, 'write',"UPDATE `whatsapp`.`stage` SET `stage` = '2' WHERE(`id` = '" + id[0] + "') and (`chatid` = '" + str(data['senderData']['chatId']) + "');")
                        WC.SendButton(str(data['senderData']['chatId']),
                                      '',
                                      buttons=FormButtons(["Повторить заказ", "Оформить первый заказ", "Перевести в чат с оператором"]),
                                      footer='выберите нужный вариант')
                elif int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 2:
                    print("Оформляем первый заказ!")
                elif int(data['messageData']['buttonsResponseMessage']['selectedButtonId']) == 3:
                    print("Уузнаем о бонусах")
                    WC.SendButton(str(data['senderData']['chatId']), 'Как получить полезные подарки?', buttons=FormButtons(
                        ["Повторить заказ", "Оформить первый заказ", "Перевести в чат с оператором"]),
                                  footer='выберите нужный вариант')
            pass
    else:
        return 200
    pass
#rint(str(FormButtons(buttons)))
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
