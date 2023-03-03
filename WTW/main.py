import telebot
import requests
import random
from telebot import types
import getMovie
import getWeather

get_film = getMovie

#from telebot import types

#бот телеги и его токен
token = '6076273456:AAFuxoL1xd9gxkEKDo1bfwgVieNZumSxSNA'
bot = telebot.TeleBot(token)

API_KEY = '1d442f5e38536b0955c89d1f7fd0f83c'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

def translate_text(text, from_lang, to_lang):
    url = 'https://api.mymemory.translated.net/get'
    params = {'q': text, 'langpair': f'{from_lang}|{to_lang}'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        translated_text = data['responseData']['translatedText']
        return translated_text
    else:
        return None


#функция получения погоды
def get_weather(lat, lon):
    params = {'lat': lat, 'lon': lon, 'appid': API_KEY}
    response = requests.get(WEATHER_URL, params = params)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        print(data)
        temperature = data['main']['temp'] - 273.15
        translated_desc = translate_text(weather_desc, 'en', 'ru')
        return translated_desc, temperature
       # return data['weather'][0]['description'], data['main']['temp'] - 273.15
    else:
        return None, None


#Создание клавиатуры
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

buttons = [
    types.KeyboardButton('Геолокация', request_location=True),
    types.KeyboardButton('Что это?'),
    types.KeyboardButton('Заролить фильмец'),
    types.KeyboardButton('Что-то еще11'),
    types.KeyboardButton('Что-то еще123'),
    types.KeyboardButton('🤡')
]

'''
button1 = telebot.types.KeyboardButton('Поделиться геолокацией', request_location = True)
button2 = telebot.types.KeyboardButton('Нажми тут')
button3 = telebot.types.KeyboardButton('ЖЖП')
'''
keyboard.add(*buttons)

#Обработка команд
@bot.message_handler(commands=['start'])
def start(message):
    text_answer = 'Давай поможем тебе выбрать че надеть.\nДля этого мне потребуется твоя геолокация, чтобы я мог глянуть погоду и подсказать\nВообще я тут все подряд решил тестить так что воооот'
    bot.send_message(message.chat.id, text_answer, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Im here to help u', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    # Кнопка Что это
    if message.text == 'Что это?':
        text_answer = '''Пилю ботиса
Сейчас есть запрос геолокации -> получение погоды на английском -> перевод и выдача ботом описания и градусы
Фильмы ролятся по рандомному запросу
В планах сделать меню с рандомным поиском после выбора жанра
        '''
        bot.send_message(message.chat.id, text_answer, reply_markup=keyboard)

    # Кнопка рандомного фильма
    elif message.text == 'Заролить фильмец':
        film = get_film.random_movie_search()
        photo = get_film.get_image(film['image'])
        if photo == 'Без фото':
            print('ERROR')
        else:
            bot.send_photo(chat_id=message.chat.id, photo=photo)

        if film['desk'] == 'None':
            bot.send_message(message.chat.id, film['name'], reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, film['name'], reply_markup=keyboard)
            bot.send_message(message.chat.id, film['desk'], reply_markup=keyboard)
            

    elif message.text == 'Что-то еще11':
        bot.send_message(message.chat.id, 'Жора Жирный Педик', reply_markup=keyboard)
    elif message.text == 'Что-то еще123':
        bot.send_message(message.chat.id, 'Жора Жирный Педик', reply_markup=keyboard)
    elif message.text == '🤡':
        bot.send_message(message.chat.id, 'Наконец то ты нажал на себя', reply_markup=keyboard)
    else:
         bot.send_message(message.chat.id, 'Тыкни в кнопку, а не пиши в чат', reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def share_geo(message):
    lat, lon = message.location.latitude, message.location.longitude
    print(lat, lon)
    weather = getWeather
    description, temperature = weather.get_weather(lat, lon)
    if description and temperature:
        response_text = f'Сейчас на улице {description}, температура {temperature:.1f} градусов'
    else:
        response_text = 'Че то не получилось'
    bot.send_message(message.chat.id, response_text)

'''

@bot.message_handler(commands=['Нажми тут'])
def command2(message):
    bot.send_message(message.chat.id, 'Пs, пока не сделано')
    
@bot.message_handler(commands=['ЖЖП'])
def command3(message):
    bot.send_message(message.chat.id, 'Жоs sd')
'''
bot.polling(none_stop=True)

