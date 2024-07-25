import telebot
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я бот для управления чатом. Напиши /help, "
                              f"чтобы узнать, что я умею.")


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, "/start - Запуск бота\n/id - узнать id своего user'а")


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        name = message.from_user.first_name
        bot.send_message(message.chat.id, f"Привет, {name}!")
    elif message.text.lower() == '/id':
        user_id = message.from_user.id
        bot.reply_to(message, user_id)


bot.polling(non_stop=True)
