import telebot
import os
from dotenv import load_dotenv
import requests

load_dotenv()

bot_token = os.getenv("TOKEN_TG")
weather_token = os.getenv("TOKEN_WEATHER")

if bot_token is None:
    raise Exception("Bot token is not defined")

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я бот для управления чатом. "
                                      f"Напиши /help, чтобы узнать, что я умею.")


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, "/start - Запуск бота\n/help - помощь\n/id - узнать id своего user'а\n"
                                      "/weather - узнать погоду")


@bot.message_handler(commands=["weather"])
def weather_command(message):
    bot.send_message(message.chat.id, "Напиши мне название города и я пришлю сводку погоды")


@bot.message_handler(content_types=['text'])
def weather(message):

    try:
        # получаем город из сообщения пользователя
        city = message.text.lower()
      # формируем запрос
        url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+f'&units=metric&lang=ru&appid={weather_token}'
      # отправляем запрос на сервер и сразу получаем результат
        weather_data = requests.get(url).json()
      # получаем данные о температуре и о том, как она ощущается
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
      # формируем ответы
        w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
        w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
      # отправляем значения пользователю
        bot.send_message(message.from_user.id, w_now)
        bot.send_message(message.from_user.id, w_feels)

    except Exception as ex:
        print(ex)


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        name = message.from_user.first_name
        bot.send_message(message.chat.id, f"Привет, {name}!")
    elif message.text.lower() == '/id':
        user_id = message.from_user.id
        bot.reply_to(message, user_id)
    else:
        bot.send_message(message.chat.id, "Не знаю такой команды")


bot.polling(non_stop=True)
