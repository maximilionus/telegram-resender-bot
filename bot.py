import telebot, dotenv, os
dotenv.load_dotenv()

def get_user_language(message):
	if (message.from_user.language_code == 'ru'):
		return 'ru'
	else:
		return 'en'

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
user_id_recipient = os.getenv("ID_RECIPIENT")

@bot.message_handler()
def message_resender(message):
	bot.send_message(user_id_recipient, "\u0060[ RECEIVED MESSAGE ]\u0060\n\n*From :* {0} {1}\n*Username :* @{2}\n*ID : * {3}".format(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.id), parse_mode="markdown")
	bot.forward_message(user_id_recipient, message.from_user.id, message.message_id)
	bot.reply_to(message, 'Your message was successfully sent to recipient')

bot.polling()