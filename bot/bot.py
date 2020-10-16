import os

import redis
import telebot

from dotenv import load_dotenv
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# from bot.pgdb import query_insert
from pgdb import query_insert
from bot.utils import get_info_barcode, save_in_redis, get_info_from_redis, get_chat_id

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_DB = os.environ.get('REDIS_DB')

bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)
redis_broker = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
data = dict()

phone_number_keyboard = types.KeyboardButton(
    text='Отправить номер телефона',
    request_contact=True
)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    data['id'] = message.chat.id

    bot.send_message(chat_id=message.chat.id, text='Здравствуйте. Введите своё Имя.')
    bot.register_next_step_handler(message=message, callback=process_phone_step)
    hash_key = get_chat_id(chat_id=data['id'], postfix='profile')

    # save_in_redis(hash_key=hash_key, fields=data, r=redis_broker)
    # print(get_info_from_redis(get_chat_id(chat_id=data['id'], postfix='profile'), redis_broker))
    # redis_broker.hset(hash_key, 'id', message.chat.id)
    # print('--')
    # print(get_info_from_redis(hash_key, redis_broker))


def process_phone_step(message):
    data['name'] = message.text
    # hash_key = get_chat_id(chat_id=message.chat.id, postfix='profile')
    # save_in_redis(hash_key=hash_key, fields=data, r=redis_broker)
    # print(get_info_from_redis(get_chat_id(chat_id=hash_key, postfix='profile'), redis_broker))
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(phone_number_keyboard)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Спасибо, {message.text}\nВведите свой телефон',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    data['phone'] = message.contact.phone_number
    bot.send_message(
        chat_id=message.from_user.id,
        text=f'Благодарю,\nТелефон получен {message.contact.phone_number}.'
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=f'теперь нужен штрихкод'
    )
    bot.register_next_step_handler(message=message, callback=handle_barcode)


@bot.callback_query_handler(func=lambda message: True)
def inline_handler(message):
    barcode = data['barcode']['data']
    message_text = ''
    if 'odd_handler' in message.data:
        message_text = barcode[1::2][0]
    if 'even_handler' in message.data:
        message_text = barcode[0::2][-1]

    bot.send_message(
        chat_id=message.from_user.id,
        text=message_text
    )


@bot.message_handler(content_types=['photo'])
def handle_barcode(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    real_filename = file_info.file_path.split('/')[-1]
    file_info.file_path = f'{message.from_user.id}-{message.date}-{real_filename}'
    filename = f'images/{file_info.file_path}'

    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(
        InlineKeyboardButton(text="Чет", callback_data='odd_handler'),
        InlineKeyboardButton(text="Нечет", callback_data='even_handler')
    )

    query_insert(table_name='profile_user_profile', **data)
    data['barcode'] = get_info_barcode(filename)

    data['barcode']['image'] = filename
    query_insert(table_name='profile_user_barcode', **data['barcode'])
    print('Штрихкод успешно сохранен')
    save_in_redis(
        hash_key=message.from_user.id,
        fields=data,
        r=redis_broker
    )
    get_info_from_redis(
        hash_key=message.from_user.id,
        r=redis_broker
    )
    barcode = data['barcode']
    bot.send_message(
        chat_id=message.from_user.id,
        text=f"найден ШК: {barcode.get('data')}",
        reply_markup=keyboard,
    )


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(chat_id=message.chat.id, text=message.text)


bot.remove_webhook()

bot.polling()
