import os
import dotenv
from termcolor import colored
dotenv.load_dotenv()

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
	bot = colored('[BOT]', 'red', attrs=['reverse'])
	print(f'{bot} {log_message}')