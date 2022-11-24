import telebot
from config import keys,TOKEN
from extensions import CryptoConverter,APIException


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    print(message.chat.username,':', message.text)
    text = 'Приветсвую!' \
        '\n Данный бот поможет тебе произвести конвертацию валют по текущему курсу' \
        '\nСписок доступных валют: /values' \
        '\n Пример конвертации: <Имя валюты, цену которой хотим узнать> <Имя валюты, за которую будем покупать> <количество первой валюты>' \
        '\n Вводить необходимо через пробел и без ковычек. Если сумма покупки дробная, то используй точку.' \
                 '\n Пример:' \
        '\n Евро Рубль 100'
    bot.reply_to(message, text)
    pass

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    print(message.chat.username,':', message.text)
    text = 'Список валют, которые можно конвертировать в настоящий момент:'
    for key in keys.keys():
        text='\n'.join((text,key))
    bot.reply_to(message, text)
    pass

@bot.message_handler(content_types=['text'])
def convert(message):
     print(message.chat.username,':', message.text)
     try:
        values = message.text.title().split(' ')

        if len(values) != 3:
            raise APIException('Проверьте корректность заполнения данных.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote,base,amount)
     except APIException as e:
         bot.reply_to(message, f'Ошибка ввода?\n {e}')
     except Exception as e:
         bot.reply_to(message, f'Не удалось обработать команду {e}')
     else:
         text = f'Цена за {amount} {quote} в {base} = {total_base}'
         bot.send_message(message.chat.id, text)


bot.polling()