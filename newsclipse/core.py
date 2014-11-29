import logging
from urlparse import urlparse

from flask import Flask
from flask.ext.assets import Environment, Bundle
from kombu import Exchange, Queue
from celery import Celery
from pymongo import MongoClient

from newsclipse import default_settings

logging.basicConfig(level=logging.DEBUG)

# specific loggers
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('pyelasticsearch').setLevel(logging.WARNING)


app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('NEWSCLIPSE_SETTINGS', silent=True)

assets = Environment(app)
mongo = MongoClient(app.config.get('MONGO_URL'))
db = mongo[urlparse(app.config.get('MONGO_URL')).path[1:]]

queue_name = 'newsclipse_q'
app.config['CELERY_DEFAULT_QUEUE'] = queue_name
app.config['CELERY_QUEUES'] = (
    Queue(queue_name, Exchange(queue_name), routing_key=queue_name),
)

celery = Celery('newsclipse', broker=app.config['CELERY_BROKER_URL'])
celery.config_from_object(app.config)


assets.register('css', Bundle('style/app.less',
                              filters='less',
                              output='assets/style.css'))

assets.register('js', Bundle("vendor/jquery/dist/jquery.js",
                            "vendor/underscore/underscore.js",
                            "vendor/backbone/backbone.js",
                            "vendor/layoutmanager/backbone.layoutmanager.js",
                            "vendor/modernizr/modernizr.js",
                            "js/app.js",
                             #filters='uglifyjs',
                             output='assets/app.js'))

assets.register('tmpl', Bundle("js/templates/test.jst",
                             filters='jst',
                             output='assets/templates.js'))
