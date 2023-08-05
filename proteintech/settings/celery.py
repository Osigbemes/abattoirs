import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proteintech.settings.base')
app = Celery('proteintech')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs. 
app.autodiscover_tasks()

# REDIS related settings 
REDIS_HOST = 'localhost' 
REDIS_PORT = '6379' 
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0' 
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'


# Set broker_connection_retry and broker_connection_retry_on_startup
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True