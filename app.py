import telebot
from TOKEN import keys, TOKEN
from extensions import APIException, CurrencyExchangeConvertion


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для начала работы введите команду в следующем формате:\n \
<имя вашей валюты><в какую валюту хотите перевести><сумма вашей валюты>\nОбратите внимание, что наименование валют вводится с маленькой буквы.\n\
Для получения списка доступных валют введите /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    keys_ = '\n'.join(keys.keys())
    text = 'Доступные валюты:\n'
    bot.reply_to(message, text+keys_)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Количество параметров неверно')

        base, quote, amount = values
        x = CurrencyExchangeConvertion.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\nПричина: {e}')
    else:
        text = f'{amount} {base} стоит {x} {quote}'
        bot.send_message(message.chat.id, text)



bot.polling()