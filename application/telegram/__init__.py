import requests

class Telegram(object):
    def __init__(self, token, chat):
        self.TOKEN = token
        self.CHAT = chat
        self.URL = "https://api.telegram.org/bot{}".format(self.TOKEN)

    def get_url(self, url):
        try:
            response = requests.get(url)
            content = response.content.decode("utf8")
            return content
        except:
            return self.get_url(url)

    def send_message(self, text):
        try:
            url = self.URL + "/sendMessage?text={}&chat_id={}".format(text, self.CHAT)
            self.get_url(url)
        except:
            return self.send_message(text)