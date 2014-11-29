import logging

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from pyelasticsearch import ElasticSearch

from newsclipse import default_settings

logging.basicConfig(level=logging.DEBUG)

# specific loggers
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('pyelasticsearch').setLevel(logging.WARNING)


app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('NEWSCLIPSE_SETTINGS', silent=True)

db = SQLAlchemy(app)
assets = Environment(app)

es = ElasticSearch(app.config.get('ELASTICSEARCH_URL'))
es_index = app.config.get('ELASTICSEARCH_INDEX', app_name)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

assets.register('css', Bundle('style/app.less',
                              filters='less',
                              output='assets/style.css'))

assets.register('js', Bundle("js/app.js",
                             #filters='uglifyjs',
                             output='assets/app.js'))
