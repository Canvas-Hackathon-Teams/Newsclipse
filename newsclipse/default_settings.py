import os

DEBUG = True
ASSETS_DEBUG = True
SECRET_KEY = 'banana pancakes'
WTF_CSRF_ENABLED = False
ELASTICSEARCH_URL = os.environ.get('BONSAI_URL', 'http://localhost:9200')
