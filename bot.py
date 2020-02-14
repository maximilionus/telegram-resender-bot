import dotenv
import telebot
import os
import helpers as h
from helpers import log_bot
from termcolor import colored

dotenv.load_dotenv()

if 'SOCKS5' in os.environ:
	if len(os.getenv('SOCKS5')) > 0:
		telebot.apihelper.proxy = {'https':'socks5://{}'.format(os.getenv('SOCKS5'))}

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
user_id_owner = os.getenv("ID_OWNER")

@bot.message_handler(commands=['start'])
def start_message_handle(message):
	bot.send_message(message.from_user.id, h.text["start"]["en"], parse_mode=h.text["start"]["_parse"]) #TODO - Add text

@bot.message_handler(commands=['help'])
def help_help_message(message):
	log_bot('Detected /start for user {}.'.format(h.format_user2log(message)))
	if h.get_user_language(message) == 'ru':
		start_message = bot.send_message(message.from_user.id, h.text["help"]["ru"], parse_mode=h.text["help"]["_parse"])
	else:
		start_message = bot.send_message(message.from_user.id, '', parse_mode=h.text["help"]["_parse"])
	if h.get_debug_status():
		str_localize = '\u0060< БОТ НА ОБСЛУЖИВАНИИ >\u0060' if h.get_user_language(message) == 'ru' else '\u0060< BOT IS UNDER MAINTENANCE >\u0060'
		start_message = bot.edit_message_text('{}\n\n'.format(str_localize) + start_message.text, message.from_user.id, start_message.message_id, parse_mode='markdown')
	if h.check_is_owner(message):
		bot.send_message(message.from_user.id, '*OWNER COMMANDS SYNTAX*\n🔴 \u0060/send : recipient_id : message_text\u0060\n🔴 \u0060$debug$\u0060 - add in the beginning of message to get message json', parse_mode='markdown')

@bot.message_handler(commands=['send'])
def owner_send_message(message):
	if h.check_is_owner(message):
		parsed_command = message.text.split(' : ')
		if len(parsed_command) == 3:
			recipient_id = parsed_command[1]
			try:
				int(recipient_id)
			except ValueError:
				bot.reply_to(message, 'Wrong \u0060ID\u0060 detected, *aborting*. Only \u0060INT\u0060 values is allowed for \u0060ID\u0060', parse_mode='markdown')
			else:
				message_text = parsed_command[2]
				notif_text_localize = '*[ YOU HAVE RECEIVED A NEW MESSAGE ]*'
				try:
					bot.send_message(recipient_id, notif_text_localize + '\n\n' + message_text, parse_mode='markdown')
					bot.reply_to(message, '*MESSAGE WAS SUCCESSFULLY SENT*', parse_mode='markdown')
					log_bot('Message from OWNER to < {0} > was successfully sent.'.format(recipient_id))
				except Exception as e:
					bot.reply_to(message, '*!!! MESSAGE WAS NOT SENT !!!*', parse_mode='markdown')
					bot.reply_to(message, str(e))
					log_bot('Message from OWNER to < {0} > not sent due to exception occured.'.format(recipient_id))

@bot.message_handler(content_types=['audio','video','photo','document','text','location','contact','sticker'])
def message_resender(message):
	if type(message.text) == str and message.text.startswith('$debug$'):
		if h.check_is_owner(message):
			bot.send_message(message.from_user.id, message)
			log_bot('{} used $debug$'.format(h.format_user2log(message)))
	elif h.get_debug_status() and not h.check_is_owner(message):
		message_localize = '<code>[ БОТ НА ОБСЛУЖИВАНИИ ]</code>\n\n<b>ПЕРЕОТПРАВЬТЕ СООБЩЕНИЕ ЧУТЬ ПОЗЖЕ</b>' if h.get_user_language(message) == 'ru' else '<code>[ BOT IS UNDER MAINTENANCE ]</code>\n\n<b>TRY TO RESEND YOUR MESSAGE A LITTLE BIT LATER</b>'
		bot.send_message(message.from_user.id, message_localize, parse_mode='HTML')
	else: 
		bot.send_message(user_id_owner, '\u0060[ RECEIVED MESSAGE ]\u0060\n\n*From :* {0} {1}\n*Username :* @{2}\n*LNG :* {3}\n*ID :* {4}'
			.format(message.from_user.first_name, message.from_user.last_name, message.from_user.username, h.get_user_language(message), message.from_user.id), parse_mode="markdown")
		bot.forward_message(user_id_owner, message.from_user.id, message.message_id)
		if h.get_user_language(message) == 'ru':
			bot.reply_to(message, '*Ваше сообщение было успешно перенаправлено получателю*',parse_mode='markdown')
		else:
			bot.reply_to(message, '*Your message was successfully forwarded to recipient*', parse_mode='markdown')
		log_bot('Message from {} to OWNER was successfully sent.'.format(h.format_user2log(message)))

log_bot("Initialized. Starting polling.")
bot.infinity_polling()
