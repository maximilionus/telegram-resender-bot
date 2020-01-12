import telebot
import dotenv
import os

dotenv.load_dotenv()

def get_user_language(message):
	if (message.from_user.language_code == 'ru'):
		return 'ru'
	else:
		return 'en'

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
user_id_recipient = os.getenv("ID_RECIPIENT")

@bot.message_handler(commands=['start'])
def starter_help_message(message):
	if get_user_language(message) == 'ru':
		bot.send_message(message.from_user.id, '*Привет* 👋\n\nДанный бот пересылает все отправленые ему сообщения сам знаешь кому. \
Бот так-же может выполнять функцию обратной связи, так что ответы на все свои вопросы ты скорее всего получишь через него.\n\nНу вот, собственно, и все. \
Можешь прямо сейчас писать сообщение и отправлять его без каких либо дополнительных команд :)\n\nБот почти всегда онлайн, но все же может иногда уходить на \
\u0022профилактику\u0022 если я вдруг решу (обновить / перезапустить / etc) его. Твое сообщение в любом случае будет доставлено после его запуска и ты получишь \
подтверждение доставки. Так что не надо отправлять одно и тоже сообщение каждые 5 минут :)', parse_mode='markdown')
	else:
		bot.send_message(message.from_user.id, '*Welcome* 👋\n\nThis bot forwards all the messages sent to it to... you know who. \
The bot can also perform a feedback function, so you will most likely get all your questions answered through it.\n\nWell, that\u0027s \
it, actually. You can write a message right now and send it without any additional commands :)\n\nThe bot is almost always online, \
but still can sometimes go on maintenance if I suddenly decide to (update / restart / etc) it. Your message will be delivered anyway \
after it\u0027s launched and you will receive a delivery confirmation. So there\u0027s no need send the same message every 5 minutes :)', parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def message_resender(message):
	bot.send_message(user_id_recipient, '\u0060[ RECEIVED MESSAGE ]\u0060\n\n*From :* {0} {1}\n*Username :* @{2}\n*ID : * {3}'
		.format(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.id), parse_mode="markdown")
	bot.forward_message(user_id_recipient, message.from_user.id, message.message_id)
	bot.reply_to(message, '*Ваше сообщение было успешно перенаправлено получателю*' if get_user_language(message) == 'ru' else '*Your message was successfully forwarded to recipient*', parse_mode='markdown')

print("[BOT] Initialized. Starting polling.")
bot.polling()