from bot.bot import Bot
from bot.handler import MessageHandler

TOKEN = "001.2924220722.2165912858:1005884797" #your token here

bot = Bot(token=TOKEN)
bot.send_text(chat_id="w.done@777-777.org", text="test")

def message_cb(bot, event):
    bot.send_text(chat_id=event.from_chat, text=event.text)


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()