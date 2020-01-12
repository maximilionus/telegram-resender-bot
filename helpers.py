import os
import dotenv
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