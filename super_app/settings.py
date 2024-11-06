import os

from config_env.base import *


PROJECT_CONFIG = config
APP_NAME = 'SUPER APP'

DEBUG = False

if DEBUG:
    from config_env.local import *
else:
    from config_env.production import *
DEBUG = True
