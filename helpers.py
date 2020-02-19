import os
import dotenv
from termcolor import colored
dotenv.load_dotenv()

# ------------------------- #

def get_user_language(message):
	if (message.from_user.language_code == 'ru'):
		return 'ru'
	else:
		return 'en'

def check_is_owner(message):
	if int(message.from_user.id) == int(os.getenv('ID_OWNER')):
		return bool(1)
	else:
		return bool(0)

def get_debug_status():
	if 'BOT_DEBUG_STATUS' in os.environ:
		if os.getenv('BOT_DEBUG_STATUS') == '1':
			return bool(1)
		elif os.getenv('BOT_DEBUG_STATUS') == '0':
			return bool(0)
	else:
		return bool(0)

def format_user2log(message):
	owner_detect = 'OWNER, ' if check_is_owner(message) else ''
	user_id = 'id:"{}"'.format(message.from_user.id)
	username = ', username:"@{}"'.format(str(message.from_user.username)) if str(message.from_user.username) != 'None' else ''
	first_name = ', first:"{}"'.format(str(message.from_user.first_name)) if str(message.from_user.first_name) != 'None' else ''
	last_name = ', last:"{}"'.format(str(message.from_user.last_name)) if str(message.from_user.last_name) != 'None' else ''
	result = f'( {owner_detect}{user_id}{username}{first_name}{last_name} )'
	return result

def log_bot(log_message = ''):
	bot = str()
	if "BOT_LOGS_DISABLE_COLOR" in os.environ:
		if os.getenv("BOT_LOGS_DISABLE_COLOR") == '1':
			bot = '[BOT]'
	else:
		bot = colored('[BOT]', 'red', attrs=['reverse'])
	print(f'{bot} {log_message}')

# ------------------------- #

text = {
	"start":{
		"_parse": None,
		"en":"👋\n\n> /help <"
	},
	"help":{
		"_parse": "markdown",
		"en": "*Welcome* 👋\n\nThis bot forwards all the messages sent to it to... you know who. The bot can also perform a feedback function, so you will most likely get all your questions answered through it.\n\nWell, that\u0027s it, actually. You can write a message right now and send it without any additional commands :)\n\nThe bot is almost always online, but still can sometimes go on maintenance if I suddenly decide to (update / restart / etc) it. Your message will be delivered anyway after it\u0027s launched and you will receive a delivery confirmation. So there\u0027s no need send the same message every 5 minutes :",
		
		"ru": "*Привет* 👋\n\nДанный бот пересылает все отправленые ему сообщения сам знаешь кому. Бот так-же может выполнять функцию обратной связи, так что ответы на все свои вопросы ты скорее всего получишь через него.\n\nНу вот, собственно, и все. Можешь прямо сейчас писать сообщение и отправлять его без каких либо дополнительных команд :)\n\nБот почти всегда онлайн, но все же может иногда уходить на \u0022профилактику\u0022 если я вдруг решу (обновить / перезапустить / etc) его. Твое сообщение в любом случае будет доставлено после его запуска и ты получишь подтверждение доставки. Так что не надо отправлять одно и то же сообщение каждые 5 минут :)",
	},
}