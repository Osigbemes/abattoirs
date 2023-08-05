import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proteintech.settings.base')
app = Celery('proteintech')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs. 
app.autodiscover_tasks()

# REDIS related settings 
REDIS_HOST = '127.0.0.1' 
REDIS_PORT = '6379' 
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0' 
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
