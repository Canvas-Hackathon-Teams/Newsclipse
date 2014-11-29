import os
PROJECT_NAME = 'Newsclipse'
PROJECT_DESCRIPTION = 'You know, an IDE for news!'
DEBUG = True
ASSETS_DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'banana pancakes')
WTF_CSRF_ENABLED = False
MONGO_URL = os.environ.get('MONGOHQ_URL', 'mongodb://localhost:27017/newsclipse')

OPENCORPORATES_TOKEN = os.environ.get('OPENCORPORATES_TOKEN')

CELERY_ALWAYS_EAGER = False
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_URL = os.environ.get('RABBITMQ_BIGWIG_URL',
                                   'amqp://guest:guest@localhost:5672//')
