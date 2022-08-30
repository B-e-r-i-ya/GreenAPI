import requests

class GreenAPI():
    idInstance = ''
    apiTokenInstance = ''
    def __init__(self, idInstance, apiTokenInstance, webhookInstance=None):
        idInstance = idInstance
        apiTokenInstance = apiTokenInstance
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


    def SendMessage(self):

        pass
