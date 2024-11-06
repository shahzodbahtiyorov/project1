from dotenv import dotenv_values
from config_env.base import *
from config_env.base import BASE_DIR
from io import StringIO

from dotenv import dotenv_values

from config_env.base import BASE_DIR
with open('./super_app/.env', 'rt') as f:
    content = f.read()
    dotenv_config = dotenv_values(stream=StringIO(content))

ALLOWED_HOSTS = eval(dotenv_config.get('ALLOWED_HOSTS'))
DEBUG = eval(dotenv_config.get('DEBUG'))
SECRET_KEY = dotenv_config.get('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ['*']
