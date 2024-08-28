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
def handle_text_message(message):
    if message.text.lower() in ['привет', 'здравствуйте']:
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!")
    elif message.text.lower() == '/id':
        bot.reply_to(message, f"Ваш ID: {message.from_user.id}")
    else:
        try:
            city = message.text.strip()
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={weather_token}'
            weather_data = requests.get(url).json()
            temperature = round(weather_data['main']['temp'])
            temperature_feels = round(weather_data['main']['feels_like'])
            bot.send_message(message.chat.id, f"Сейчас в городе {city} {temperature} °C, ощущается как {temperature_feels} °C.")
        except KeyError:
            bot.send_message(message.chat.id, "Не удалось найти город. Проверьте правильность названия.")
        except requests.exceptions.RequestException:
            bot.send_message(message.chat.id, "Ошибка при подключении к серверу погоды. Попробуйте позже.")
        except Exception as ex:
            bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте снова.")
            print(ex)


bot.polling(non_stop=True)
