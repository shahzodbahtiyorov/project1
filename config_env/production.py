# settings/production.py

from io import StringIO
import sentry_sdk
from dotenv import dotenv_values

with open('/super_app/.env', 'rt') as f:
    content = f.read()
    dotenv_config = dotenv_values(stream=StringIO(content))

ALLOWED_HOSTS = eval(dotenv_config.get('ALLOWED_HOSTS'))
DEBUG = eval(dotenv_config.get('DEBUG'))
SECRET_KEY = dotenv_config.get('SECRET_KEY')


sentry_sdk.init(
    dsn="https://bc6f2000748fa550c17251292a56d0e2@sentry.cloudgate.uz/7",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=0.5,
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': dotenv_config.get('POSTGRES_DATABASE'),
        'USER': dotenv_config.get('POSTGRES_USERNAME'),
        'PASSWORD': dotenv_config.get('POSTGRES_PASSWORD'),
        'HOST': dotenv_config.get('POSTGRES_MASTER_HOST'),
        'PORT': dotenv_config.get('POSTGRES_MASTER_PORT'),
        'OPTIONS': {

            'application_name':'superapp'



        }
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': dotenv_config.get('POSTGRES_REPLICA_HOST'),
        'NAME': dotenv_config.get('POSTGRES_DATABASE'),
        'USER': dotenv_config.get('POSTGRES_USERNAME'),
        'PASSWORD': dotenv_config.get('POSTGRES_PASSWORD'),
        'PORT': dotenv_config.get('POSTGRES_REPLICA_PORT'),
        'OPTIONS': {

            'application_name':'superapp',


        }
    }
}

DEFAULT_FILE_STORAGE = 'django_minio_backend.models.MinioBackend'
STATICFILES_STORAGE = 'django_minio_backend.models.MinioBackendStatic'
MINIO_MEDIA_FILES_BUCKET = 'app-superapp'
MINIO_STATIC_FILES_BUCKET = 'app-superapp'
MINIO_ENDPOINT = dotenv_config.get('CDN_URL')
MINIO_REGION = dotenv_config.get('CDN_REGION')
MINIO_ACCESS_KEY = dotenv_config.get('CDN_ACCESS_KEY')
MINIO_SECRET_KEY = dotenv_config.get('CDN_SECRET_KEY')
MINIO_USE_HTTPS = True
MINIO_PUBLIC_BUCKETS = ['app-superapp']

CELERY_BROKER_URL = f'redis://{dotenv_config.get("REDIS_HOST")}:6379/{dotenv_config.get("REDIS_DB")}'
CELERY_RESULT_BACKEND = f'redis://{dotenv_config.get("REDIS_HOST")}:6379/{dotenv_config.get("REDIS_DB")}'
USE_REPLICA_DATABASE = True
