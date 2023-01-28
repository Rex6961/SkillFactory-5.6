import telebot
from config import keys
from extensions import ConvertionException, CryptoConverter
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.environ.get('TOKEN'))


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Добро пожаловать в конвертор валют.\n\
Чтобы увидеть список доступных валют нажмите /values.\n\
Что бы узнать стоимость валюты введите\n\
                                    пример: рубль доллар 1'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Не правильное количество параметров")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
