import os

import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("PUT YOUR TOKEN HERE")
DEBUG = True
app = Flask(__name__)


@bot.callback_query_handler(func=lambda call: "id_YouTube" == call.data)
def azione1(message):
    bot.send_message(message.message.chat.id, "https://www.youtube.com/c/PythonBiellaGroup")


@bot.callback_query_handler(func=lambda call: "id_GitHub" == call.data)
def azione2(message):
    bot.send_message(message.message.chat.id, "https://github.com/PythonGroupBiella/")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Benvenuto e buon uso del bot PythonBiellaGroup!")


@bot.message_handler(commands=['links'])
def keyboard(message):
    markup = ReplyKeyboardMarkup(row_width=2)
    itembtn1 = KeyboardButton('YouTube')
    itembtn2 = KeyboardButton('GitHub')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Quale link vuoi?", reply_markup=markup)


@bot.message_handler(func=lambda m: "python" in m.text)
def fun2(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Link YouTube", callback_data="id_YouTube"),
               InlineKeyboardButton("Link GitHub", callback_data="id_GitHub"))

    bot.send_message(message.chat.id, "Hai scritto python?", reply_markup=markup)


# Gestione temporanea del comando links
@bot.message_handler(func=lambda m: True)
def fun_generale(message):
    if "YouTube" in message.text:
        bot.reply_to(message, "https://www.youtube.com/c/PythonBiellaGroup")
    else:
        bot.reply_to(message, "https://github.com/PythonGroupBiella/")


# Webhook con Flask
@app.route("/webhook", methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=['GET'])
def get_home():
    return "!", 200

def set_webhook():
    bot.remove_webhook()
    bot.set_webhook("https://provapythonbiellagroup.herokuapp.com/webhook")


if __name__ == '__main__':
    if DEBUG:
        bot.remove_webhook()
        bot.polling()
    else:
        set_webhook()
        app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
