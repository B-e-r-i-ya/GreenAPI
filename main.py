import requests

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
                          "\r\n\t\"markIncomingMessagesReaded\": \"no\"," \
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

#rint(str(FormButtons(buttons)))
WC = GreenAPI("1101754804", "d660db8008434810a96c21062cd770d2e24ed3415d534f9fae")
test = WC.SendButton(chatId="79237246968@c.us", message="Херня", buttons=FormButtons(buttons), footer="Нажми")
print(test.text.encode('utf8'))

