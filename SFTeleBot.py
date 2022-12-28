# Здравствтуйте, предыдущие работы хотел сделать по красоте, но обленился и скопировал. Сейчас покажу как я пишу.
# Импорт и подготовка к работе.
import telebot
from config import keys, tg_bot_token
from utils import ConvertionException, CurrencyConverter


bot = telebot.TeleBot(tg_bot_token)

# Основные команды
@bot.message_handler(commands=['start'])  #Приветствие пользователя.
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.chat.first_name} я бот по конвертации валют. Для \
    ознакомления введите/нажмите на команду /help\nПросмотр доступных валют /values', parse_mode='html')


@bot.message_handler(commands=['help'])  #Помощь.
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Для работы с ботом необходимо ввести 3 параметра:\n1.Введите валюту которую нужно\
                                       конвертировать\n2.Введите валюту конвертации\n3.Введите количество\
                                      \n\nПример ввода\nrub\nusd\n100', parse_mode='html')


@bot.message_handler(commands=['values'])  #Валюты.
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convertation(message: telebot.types.Message):
    vals = message.text.split(' ')

    if len(vals) != 3:
        raise ConvertionException('Слишком много параметров')

    base, quote, amount = vals
    total_base = CurrencyConverter.convert(quote, base, amount)

    text = f'{base} в {quote} в количестве {amount} \nИтог {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
