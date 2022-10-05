import requests
import json

from os import abort
from flask import Flask, request
from pymemcache.client import base
from datetime import datetime
from requests.auth import HTTPBasicAuth
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
#============================Class===========================================

TOKEN = "001.4085375959.2023817724:1003728479"  # your token here
botmyteam = Bot(token=TOKEN)

class whatsapp_class():

    '''
    Класс для взаимодействия с API GreenAPI для Whatsapp
    Подразумевается что API настроена на отправку данных через webhook
    '''
    idInstance = ""
    apiTokenInstance = ""
    headers = {
        'Content-Type': 'application/json'
    }
    client = base.Client(('localhost', 11211))
    stage2_repeate_yes = ["да", "lf", "1"]
    stage2_repeate_no = ["нет", "ytn", "2"]
    numbers_emoji = {"0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"}
    def __doc__(self):
        pass
    def __init__(self, idInstance, apiTokenInstance):
        '''
        При содании экземпляра класса переназначаем переменные
        :param idInstance: переменные полученные у GreenApi(19120)
        :param apiTokenInstance: переменные полученные у GreenApi(c2d8f72b763ed94d6159e877ef852cd61752be8f0530ae0f77)
        '''
        self.idInstance = idInstance
        self.apiTokenInstance = apiTokenInstance

    def work_schedule(self):
        rab_time = ["8", "21"]
        if int(rab_time[0]) <= int(datetime.now().hour) and int(datetime.now().hour) <= int(rab_time[1]):
            # print("Рабочее время!")
            return True
        else:
            # print("Не рабочее время!")
            return False

    def oneCapi(self, phonnuber):
        '''
        Функция
        :param phonnuber: номер клиента
        :return: возвращает json c данными о последнем заказе, либо с ошибкой
        '''
        if self.client.get(str(request.json['senderData']['chatId']+"_json")) is None:
            auth = HTTPBasicAuth('myteam', '777777')
            url = 'http://192.168.125.62:8088/trade_razrab4/hs/atczak/getdatetimechat/' + phonnuber + ''
            resp = requests.get(url=url, auth=auth)
            content = resp.json()
            self.client.set(str(request.json['senderData']['chatId'] + "_json"),
                            json.dumps(content).encode(
                                'UTF-8'), 60)
            return content
        else:
            return json.loads(self.client.get(str(request.json['senderData']['chatId']+"_json")).decode('UTF-8'))

    def new_order(self, request):
        resp = requests.post(url='https://botapi.777-777.org/v1/neworder',
                             headers={'Authorization': 'RCh6tsWymuuGP7VZh3HYsNWLwckMVnVn'},
                             json=users_data[str(request.json["senderData"]["chatId"])]['new_order'])
        return resp

    def phone(self, phone):
        phone = phone.replace('@c.us', '')
        if len(phone) == 12:
            phone = phone[2:]
        elif len(phone) == 11:
            phone = phone[1:]
        return phone

    def greeting_generator(self):
        if 5 <= int(datetime.now().hour) <= 10:
            greeting = "Доброе утро!"
        elif 11 <= int(datetime.now().hour) <= 17:
            greeting = "Добрый день!"
        elif 18 <= int(datetime.now().hour) <= 21:
            greeting = "Добрый вечер!"
        elif 22 <= int(datetime.now().hour) <= 23 or 0 <= int(datetime.now().hour) <= 4:
            greeting = "Доброй ночи!"
        return greeting

    def repeat_order_message(self, text):
        if text == "1":
            return True
        else:
            return False

    def controller(self, request):
        if request.json['typeWebhook'] == 'incomingMessageReceived' and (self.client.get(str(request.json['senderData']['chatId']) + '_manager') is not None or self.client.get(str(request.json['senderData']['chatId']) + '_manager') == True):
        #if self.client.get(str(request.json['senderData']['chatId']) + '_manager') == b'True':
            '''
            Проверяем нужно ли переводить на оператора или отдаем управления боту
            '''
            print("Перевожу сообщение на оператора!")
            print(self.client.get(str(request.json['senderData']['chatId']) + "_vkteams_manager_uid"))
            botmyteam.send_text(chat_id=self.client.get(str(request.json['senderData']['chatId'])+'_vkteams_manager_uid'),
                                text=str(request.json['senderData']['chatId'])+": "+str(request.json['messageData']['textMessageData']['textMessage']),
                                inline_keyboard_markup="{}".format(json.dumps([
                                    [
                                        {"text": "История сообщений", "callbackData": "history_messages", "style": "primary"},
                                        {"text": "Завершить диалог", "callbackData": "close_dialog", "style": "primary"}
                                    ]
                                ])))

        else:
            if request.json['typeWebhook'] == 'incomingMessageReceived':
                self.incomingMessageReceived(request)

    def editing_time(self, time_editer):
        temp = time_editer.split()
        time_editer = "c " + str(datetime.strptime(temp[0], '%Y-%m-%dT%H:%M:%S').hour) + " до " + str(
            datetime.strptime(temp[1], '%Y-%m-%dT%H:%M:%S').hour)
        return time_editer

    def mounth(self, mounth):
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

    def nomenklature(self):
        #print(self.oneCapi(self.phone(request.json['senderData']['chatId'])))
        nomenklature = ""
        for i in self.oneCapi(self.phone(request.json['senderData']['chatId']))[2]:
            #print(i["nomenclature"]+" "+str(i["quantity"]))
            nomenklature = nomenklature+i["nomenclature"]+" "+str(i["quantity"])+'шт.\\n'
            nomenklature = nomenklature.replace('"', ' \'')
        return nomenklature

    def incomingMessageReceived(self, request):
        #print("Вводные:")
        #print(self.client.get(str(request.json['senderData']['chatId']+"_jivo")))
        #print(request.json['messageData']['textMessageData']['textMessage'])
        #print(self.client.get(str(request.json['senderData']['chatId'])+'_stage').decode('UTF-8'))
        #bot.sendmessagetext(request.json['senderData']['chatId'],request.json['messageData']['textMessageData']['textMessage'])
        if not(self.client.get(str(request.json['senderData']['chatId'])+"_jivo") is None) or self.client.get(str(request.json['senderData']['chatId']+"_jivo")) == True:
            if int(self.client.get(str(request.json['senderData']['chatId']+"_jivo"))) == 1:
                #managers = ['stilet@777-777.org']
                #jivosite.sendmessage(str(request.json['senderData']['chatId']), text=str(request.json['messageData']['textMessageData']['textMessage']))
                #https://myteam.mail.ru/bot/v1/messages/sendText?token=001.3537475893.1318737291:750764880&chatId=stilet@777-777.org&text=1

                #for item in managers:
                    #requests.get('https://myteam.mail.ru/bot/v1/messages/sendText?token=001.3537475893.1318737291:750764880&chatId='+ item +'&text=' + "Сообщение от " + str(request.json['senderData']['chatId']) + ":\n" + str(request.json['messageData']['textMessageData']['textMessage']) + '')

                botmyteam.send_text(chat_id='AoLHu9Bd1_KuLooKQAQ', text="Клиенту "+str(request.json['senderData']['chatId'])+" нужна помощь!", inline_keyboard_markup="{}".format(json.dumps([
                                                     [
                                                      {"text": "Взять в работу", "callbackData": "take_to_work", "style": "primary"}
                                                     ]
                                                        ])))
                pass
        else:
            if self.client.get(str(request.json['senderData']['chatId'])) is None:
                '''
                Проверяем ключ с ид чата в мэмкэш, если нет последнее начало общения было более 12 назад, начинаем диалог с Приветствия
                '''
                print("Создаем данны в memcashed!")
                self.client.set(str(request.json['senderData']['chatId']), True, 43200) #создаем ключ с ид чата , время жизни 12 часов
                bot.sendmessagetext(request.json['senderData']['chatId'],
                                    ''+self.greeting_generator()+'\\n'
                                    'Меня зовут Ева👩🏼‍💼, я электронный менеджер по приему *заказов воды «Легенда жизни»*\\n' 
                                    'Для нашего общения, я подготовила удобное меню\\n'
                                    '👉🏻пришлите, пожалуйста, в ответном сообщении цифру соответствующую выбранному пункту:\\n\\n'
                                    ''+str(self.numbers_emoji["1"])+' - 🔁 повторить последний заказ\\n'
                                    ''+str(self.numbers_emoji["2"])+' - 💙оформить первый заказ \\n'
                                    ''+str(self.numbers_emoji["3"])+' - 🙌узнать о бонусах за онлайн-заказы\\n'
                                    ''+str(self.numbers_emoji["4"])+' - 🙎‍♀️Перевести на чат с оператором')
                self.client.set(str(request.json['senderData']['chatId'])+'_stage', 1, 90) # Переводим диалог на 1 этап
                self.client.set(str(request.json['senderData']['chatId']) + '_stage_marker', True, 1000)
            else:
                '''
                В противном случае просто спрашиваем чем помочь?
                '''
                #print(self.client.get(str(request.json['senderData']['chatId']) + '_stage'))
                if self.client.get(str(request.json['senderData']['chatId']) + '_stage') is None and self.client.get(str(request.json['senderData']['chatId']) + '_stage_marker') == b'True':
                    bot.sendmessagetext(request.json['senderData']['chatId'], "Время ожидания ответа превышено!")
                    self.client.set(str(request.json['senderData']['chatId']) + '_stage_marker', False, 10)
                if self.client.get(str(request.json['senderData']['chatId']) + '_stage') is None:
                    bot.sendmessagetext(request.json['senderData']['chatId'], "Чем могу помочь?\\n\\n"
                                                                              ""+str(self.numbers_emoji["1"])+" - 🔁 повторить последний заказ\\n"
                                                                              ""+str(self.numbers_emoji["2"])+" - 💙оформить первый заказ \\n"
                                                                              ""+str(self.numbers_emoji["3"])+" - 🙌узнать о бонусах за онлайн-заказы\\n"
                                                                              ""+str(self.numbers_emoji["4"])+" - 🙎‍♀️Перевести на чат с оператором")
                    self.client.set(str(request.json['senderData']['chatId']) + '_stage', 1, 90) # Переводим диалог на 1 этап
                    self.client.set(str(request.json['senderData']['chatId']) + '_stage_marker', True, 1000)
                else:
                    if (self.client.get(str(request.json['senderData']['chatId'])+'_stage')).decode('UTF-8') == '1' and \
                            (self.repeat_order_message(request.json['messageData']['textMessageData']['textMessage'])) == True and\
                            request.json['messageData']['textMessageData']['textMessage'] == '1':
                        resp = self.oneCapi(self.phone(request.json['senderData']['chatId']))
                        '''
                        Если 1 этап и выбран 1 пункт меню
                        '''
                        if not ("error" in resp):
                            '''
                            Если нет ошибок в ответе API 1С, начинаем диалог на повтор заказа
                            '''
                            message_temp = "В прошлый раз Вы заказывали:\\n"+self.nomenklature()+"\\n Повторим заказ?\\n\\n "+str(self.numbers_emoji["1"])+" - Да\\n "+str(self.numbers_emoji["2"])+" - Нет"
                            bot.sendmessagetext(request.json['senderData']['chatId'], message_temp)
                            self.client.set(str(request.json['senderData']['chatId']) + '_stage', 2,
                                            90)  # Переводим диалог на 2 этап
                        else:
                            print("Есть ошибки")
                            if resp["error"] in ["Нет партнера с таким номером телефона", "Более одного партнера с главным номером", "Партнер не является физическим лицом", "Нет адреса доставки подходящего критериям", "Более одного адреса доставки", "В адресе доставки не указана зона доставки"]:
                                print(resp["error"])
                                bot.sendmessagetext(request.json['senderData']['chatId'],
                                                    "К сожалению, Ваш номер не привязан к функции «Повторить заказ».\\n" 
                                                    "Привязать его можно прямо сейчас. Это займёт всего 2 минуты.\\n"
                                                    "Напишите данные, которые Вы используете при заказе воды:\\n"
                                                    "- Фамилия, имя, отчество / Наименование организации\\n"
                                                    "- Адрес доставки\\n")
                                self.client.set(str(request.json['senderData']['chatId']) + "_jivo", 1)

                            elif resp["error"] in ["У партнера есть заказ на вчера, сегодня, завтра", "У партнера последний заказ не соответствующий критериям", "У партнера в последнем заказе есть товар не соответствующий критериям"]:
                                print(resp["error"])
                                if self.work_schedule() == True:
                                    bot.sendmessagetext(request.json['senderData']['chatId'],   "К сожалению, Ваш последний заказ не подходит по параметрам для автоматического повторения.\\n"
                                                                                                "Оставайтесь в диалоге, оператор подключиться к Вам в течение  2 минут.\\n"
                                                                                                "Чтобы не ждать ответа оператора оформите свой заказ на сайте прямо сейчас:\\n"
                                                                                                " https://777-777.org\\n")
                                    self.client.set(str(request.json['senderData']['chatId']) + "_jivo", 1)
                                    botmyteam.send_text(chat_id='AoLHu9Bd1_KuLooKQAQ', text="Клиенту " + str(
                                        request.json['senderData']['chatId']) + " нужна помощь!",
                                                        inline_keyboard_markup="{}".format(json.dumps([
                                                            [
                                                                {"text": "Взять в работу",
                                                                 "callbackData": "take_to_work", "style": "primary"}
                                                            ]
                                                        ])))

                                    #self.client.set(str(request.json['senderData']['chatId']) + '_manager', True)
                                elif self.work_schedule() == False:
                                    bot.sendmessagetext(request.json['senderData']['chatId'],
                                                        "К сожалению, Ваш последний заказ не подходит по параметрам для автоматического повторения.\\n"
                                                        "Передаю данные для обработки оператору. Оператор ответит Вам завтра в рабочее время. \\n"
                                                        "Чтобы не ждать ответа оператора оформите свой заказ на сайте прямо сейчас:\\n"
                                                        " https://777-777.org\\n")
                                    self.client.set(str(request.json['senderData']['chatId']) + '_manager', True)
                                    botmyteam.send_text(chat_id='AoLHu9Bd1_KuLooKQAQ', text="Клиенту " + str(
                                        request.json['senderData']['chatId']) + " нужна помощь!",
                                                        inline_keyboard_markup="{}".format(json.dumps([
                                                            [
                                                                {"text": "Взять в работу",
                                                                 "callbackData": "take_to_work", "style": "primary"}
                                                            ]
                                                        ])))
                            else:
                                pass
                    elif str(request.json['messageData']['textMessageData']['textMessage']) == '2' and (self.client.get(str(request.json['senderData']['chatId'])+'_stage')).decode('UTF-8') == '1':

                        #elf.client.set(str(request.json['senderData']['chatId']) + '_manager_reason', "Хочет оформить первый заказ")
                        if self.work_schedule() == True:
                            #рабочее время
                            self.sendmessagetext(request.json['senderData']['chatId'], "Ух ты, первый заказ!\\n"
                                                                                        "Наши операторы умеют делать такие заказы профессионально!\\n\\n"
                                                                                        "Перевожу Вас на чат с оператором) \\n"
                                                                                        "Оставайтесь в диалоге, Вам ответят в течение 2 минут.\\n"
                                                                                        "А я прощаюсь с Вами, было приятно пообщаться!")
                            self.client.set(str(request.json['senderData']['chatId']) + '_manager', True)
                            botmyteam.send_text(chat_id='AoLHu9Bd1_KuLooKQAQ', text="Клиент " + str(
                                request.json['senderData']['chatId']) + " хочет оформить первый заказ",
                                                inline_keyboard_markup="{}".format(json.dumps([
                                                    [
                                                        {"text": "Взять в работу", "callbackData": "take_to_work",
                                                         "style": "primary"}
                                                    ]
                                                ])))
                        elif self.work_schedule() == False:
                            # не рабочее время
                            pass
                        pass

                    elif str(request.json['messageData']['textMessageData']['textMessage']) == '3' and (
                    self.client.get(str(request.json['senderData']['chatId']) + '_stage')).decode('UTF-8') == '1':
                        '''
                        узнать о бонусах за онлайн-заказы
                        '''
                        pass

                    elif str(request.json['messageData']['textMessageData']['textMessage']) == '4' and (
                    self.client.get(str(request.json['senderData']['chatId']) + '_stage')).decode('UTF-8') == '1':
                        '''
                       Перевести на чат с оператором
                        '''
                        self.client.set(str(request.json['senderData']['chatId']) + '_manager', True)
                        botmyteam.send_text(chat_id='AoLHu9Bd1_KuLooKQAQ', text="Клиент " + str(
                            request.json['senderData']['chatId']) + " хочет оформить первый заказ",
                                            inline_keyboard_markup="{}".format(json.dumps([
                                                [
                                                    {"text": "Взять в работу", "callbackData": "take_to_work",
                                                     "style": "primary"}
                                                ]
                                            ])))
                        pass

                    elif (self.client.get(str(request.json['senderData']['chatId'])+'_stage')).decode('UTF-8') == '2':
                        if (request.json['messageData']['textMessageData']['textMessage']) in self.stage2_repeate_yes:
                            self.client.set(str(request.json['senderData']['chatId']) + '_new_make_order_json', "{ ")
                            i = ''
                            number = 1
                            date_delivery = ""
                            date = {}
                            for item in self.oneCapi(self.phone(request.json['senderData']['chatId']))[1]:
                                if i != item['date']:
                                    date_delivery = date_delivery + str(self.numbers_emoji[str(number)]) + " - " + (str(datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S').day)+" "+str(self.mounth(datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S').month))) + '\\n'
                                    date[str(number)] = item['date']
                                    number = number + 1
                                i = item['date']

                            print(type(date))
                            self.client.set(str(request.json['senderData']['chatId']) + '_date_delyveri', date)
                            bot.sendmessagetext(request.json['senderData']['chatId'], 'Мы уже готовы доставить «Легенду» по адресу \\n'
                                                                                      ' '+self.oneCapi(self.phone(request.json['senderData']['chatId']))[0]['address']+'\\n'
                                                                                      'Просто выберите дату:\\n\\n'
                                                                                      ''+ date_delivery +'')
                            self.client.set(str(request.json['senderData']['chatId']) + '_stage', 3,
                                            90)  # Переводим диалог на 3 этап
                        elif (request.json['messageData']['textMessageData']['textMessage']) in self.stage2_repeate_no:
                            bot.sendmessagetext(request.json['senderData']['chatId'],
                                                ' Правильно!\\n' 
                                                'Зачем повторять последний заказ, если можно оформить новый на нашем сайте!\\n'
                                                'Широкий ассортимент, бонусы за каждый заказ! Что может быть лучше?!\\n'
                                                'https://777-777.org \\n'
                                                'Оформляйте заказы на сайте,'
                                                'или пишите мне) \\n С Вами всегда приятно пообщаться!')
                            self.client.set(str(request.json['senderData']['chatId']) + '_stage', 0,
                                            90)  # Переводим диалог на 3 этап
                    elif (self.client.get(str(request.json['senderData']['chatId']) + '_stage')).decode('UTF-8') == '3':
                        #print(request.json['messageData']['textMessageData']['textMessage'])
                        #print(self.client.get(str(request.json['senderData']['chatId']) + '_date_delyveri').decode('UTF-8'))
                        #print(self.oneCapi(self.phone(request.json['senderData']['chatId'])))
                        #print(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_date_delyveri').decode('utf-8').replace("'", "\""))["1"])
                        self.client.append(str(request.json['senderData']['chatId']) + '_new_make_order_json', '\"date\": \"' + str(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_date_delyveri').decode('utf-8').replace("'", "\""))["1"]) + '\" }')
                        #print(self.client.get(str(request.json['senderData']['chatId']) + '_new_make_order_json'))
                        #print(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_date_delyveri').decode('utf-8').replace("'", "\"")))
                        number = 1
                        time_delivery = ""
                        timeFrom = {}
                        timeBy = {}
                        print(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_date_delyveri').decode('utf-8').replace("'", "\""))[request.json['messageData']['textMessageData']['textMessage']])
                        for item in self.oneCapi(self.phone(request.json['senderData']['chatId']))[1]:
                            if item["date"] == json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_date_delyveri').decode('utf-8').replace("'", "\""))[request.json['messageData']['textMessageData']['textMessage']]:
                                print(item["dateFrom"])
                                time_delivery = time_delivery + str(self.numbers_emoji[str(number)]) + " - C " + (str(datetime.strptime(item['dateFrom'], '%Y-%m-%dT%H:%M:%S').hour) + " до " + str(datetime.strptime(item['dateBy'], '%Y-%m-%dT%H:%M:%S').hour)) + '\\n'
                                timeFrom[str(number)] = item['dateFrom']
                                timeBy[str(number)] = item['dateBy']
                            number = number + 1
                        self.client.set(str(request.json['senderData']['chatId']) + '_timeFrom', timeFrom)
                        self.client.set(str(request.json['senderData']['chatId']) + '_timeBy', timeBy)
                        bot.sendmessagetext(request.json['senderData']['chatId'],
                                            'Какое время будет удобно?\\n\\n'
                                            '' + time_delivery + '')
                        self.client.set(str(request.json['senderData']['chatId']) + '_stage', 4,
                                        90)  # Переводим диалог на 3 этап
                        self.client.delete(str(request.json['senderData']['chatId']) + '_date_delyveri')
                    elif (self.client.get(str(request.json['senderData']['chatId']) + '_stage')).decode('UTF-8') == '4':

                        #print(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_timeFrom').decode('utf-8').replace("'", "\""))[request.json['messageData']['textMessageData']['textMessage']])
                        #print(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_new_make_order_json').decode('utf-8'))["date"])
                        #print(self.oneCapi(self.phone(request.json['senderData']['chatId']))[3])
                        # http://192.168.125.62:8088/trade_razrab4/hs/atczak/makeorderchat/00-00015798/2022-05-18T00:00:00/2022-05-18T17:01:00/2022-05-18T19:00:00
                        print(self.client.get(str(request.json['senderData']['chatId']) + '_make_order'))
                        if self.client.get(str(request.json['senderData']['chatId']) + '_make_order') == b'True':
                            bot.sendmessagetext(request.json['senderData']['chatId'], "Создаю заказ, ожидайте")
                        elif self.client.get(str(request.json['senderData']['chatId']) + '_make_order') == b'success':
                            bot.sendmessagetext(request.json['senderData']['chatId'], "Уже есть заказ")
                        else:
                            self.client.set(str(request.json['senderData']['chatId']) + '_make_order', True, 43200)
                            auth = HTTPBasicAuth('myteam', '777777')
                            url = "http://192.168.125.62:8088/trade_razrab4/hs/atczak/makeorderchat/"+ str(self.oneCapi(self.phone(request.json['senderData']['chatId']))[3]["kodpartner"]).replace(' ', '') + "/" \
                                    "" + str(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_new_make_order_json').decode('utf-8'))["date"])+"/" \
                                  "" + str(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_timeFrom').decode('utf-8').replace("'", "\""))[request.json['messageData']['textMessageData']['textMessage']]) + "/" \
                                        "" + str(json.loads(self.client.get(str(request.json['senderData']['chatId']) + '_timeBy').decode('utf-8').replace("'", "\""))[request.json['messageData']['textMessageData']['textMessage']])
                            #print(url)
                            resp = requests.get(url=url, auth=auth)
                            #print(resp.json())
                            print(json.loads(json.dumps(resp.json()))[1]['success'])
                            if 'success' in json.loads(json.dumps(resp.json()))[1]:
                                self.client.set(str(request.json['senderData']['chatId']) + '_make_order', 'success', 43200)
                                nomenclature = ""
                                price =0
                                for item in json.loads(json.dumps(resp.json()))[0]:
                                    print(item)
                                    nomenclature = nomenclature + str(item['nomenclature']).replace('"', ' \'') + " " + str(item['quantity']) + "\\n"
                                    price = price + item['price']
                                    form_of_payment = item['form_of_payment']

                                print(nomenclature)
                                print(price)
                                print(form_of_payment)
                                message = "Доставим \\n" + str(nomenclature) + "шт. \\nсумма: " + str(price) + " способ оплаты " + str(form_of_payment)
                                print(message)
                                bot.sendmessagetext(request.json['senderData']['chatId'], "Доставим \\n" + str(nomenclature) + "сумма: " + str(price) + " способ оплаты " + str(form_of_payment))
                                #bot.sendmessagetext(str(request.json['senderData']['chatId']), str())
                                self.client.set(str(request.json['senderData']['chatId']) + '_stage_marker', False, 10)
                            else:
                                return "ok"
                            #print(json.dumps(resp.json())[1])

                            pass


    def outgoingMessageReceived(self, request):
        pass

    def outgoingMessageStatus(self, request):
        pass

    def stateInstanceChanged(self, request):
        pass

    def statusInstanceChanged(self, request):
        pass

    def deviceInfo(self, request):
        pass

    def incomingCall(self, request):
        pass

    def url_generation(self, metod):
        url = "https://api.green-api.com/waInstance"+self.idInstance+"/"+metod+"/"+self.apiTokenInstance+""
        return url

    def sendmessagetext(self, chatId, message):
        print("Начинаем отправку!")
        payload = ("{\r\n\t\"chatId\": \""+str(chatId)+"\",\r\n\t\"message\": \""+str(message)+"\"\r\n}").encode('utf8')
        response = requests.request("POST", self.url_generation("SendMessage"), headers=self.headers, data=payload)
        print(response.json())
        return response

    def get_an_avatar(self, id):
        payload = ('{"chatId": "'+id+'"}').encode('utf8')
        response = requests.request("POST", self.url_generation("GetAvatar"), headers=self.headers, data=payload)
        return response

class jivosite():
    url = ""
    def __init__(self, url):
        self.url = url

    def new_chat(self, id):
        '''
        Отправляем первое сообщение в живосайт, в нем должен быть передан предшествующий
        диалог с роботом
        :return:
        '''
        message = []
        payload = {}
        headers = {}

        response_outgoing = requests.request("GET",
                                             "https://api.green-api.com/waInstance10353/lastOutgoingMessages/e8ba72e6615f9b238f1d46ffb8a6085e63c24c18c5224ab490",
                                             headers=headers, data=payload)
        response_incoming = requests.request("GET",
                                             "https://api.green-api.com/waInstance10353/lastIncomingMessages/e8ba72e6615f9b238f1d46ffb8a6085e63c24c18c5224ab490",
                                             headers=headers, data=payload)

        for i in response_outgoing.json():
            if i["chatId"] == id and i["typeMessage"] == "textMessage":
                # print(i["textMessage"])
                message.append(
                    {"type": i["type"], "timestamp": i["timestamp"], "textMessage": i["textMessage"]}
                )

        for item in response_incoming.json():
            if item["chatId"] == id and item["typeMessage"] == "textMessage":
                # print(item["textMessage"])
                message.append(
                    {"type": item["type"], "timestamp": item["timestamp"], "textMessage": item["textMessage"]}
                )
        timemessage = []
        for i in message:
            timemessage.append(i["timestamp"])
        timemessage.sort()
        text = []
        for i in timemessage:
            for item in message:
                if item['timestamp'] == i:
                    if item["type"] == "incoming":
                        #print("\033[31m {}".format(item["textMessage"]))
                        text.append(item["textMessage"])
                    else:
                        #print("\033[34m {}".format(item["textMessage"]))
                        text.append(item["textMessage"])
        print(text)
        self.sendmessage(id, text=text)

    def sendmessage(self, id, name=None, photo=None, phone=None, email=None, invite=None, text=None):
        '''
        Отправка сообщения в Jivosite
        :param id:
        :param name:
        :param photo:
        :param phone:
        :param email:
        :param invite:
        :param text:
        :return:
        '''
        payload = ('{"sender" :{"id":"'+id+'", "name":"'+name+'", "photo":"'+photo+'", "phone":"'+phone+'", "email":"'+email+'", "invite" : "'+invite+'"},"message" :{ "type" : "text","id": "customer_message_id","text" : "'+text+'" } }').encode('utf8')
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", self.url, headers=headers, data=payload)
        return response



jivo = jivosite('https://joint.jivosite.com/IF6YK0nYgC56npYB/HQhStQV1oY')
bot = whatsapp_class("10353", "e8ba72e6615f9b238f1d46ffb8a6085e63c24c18c5224ab490")

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello():
    if not request.json:
        abort(400)
    else:
        if request.headers['Authorization'][7:] == "#yT4<kXRiPAeTp%5()suuqSGWbfyUf6k": #проверяем токен
            #print(request.json)
            bot.controller(request) # Пересылаем в конроллер
            return "200"
        else:
            return "Не угадал", 440

@app.route('/jivo', methods=['POST'])
def hello1():
    if not request.json:
        abort(400)
    else:
        print(request.json)
        return "200"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9003)
