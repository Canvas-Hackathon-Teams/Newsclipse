import logging

from flask import Flask
from flask.ext.assets import Environment, Bundle
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

assets = Environment(app)

es = ElasticSearch(app.config.get('ELASTICSEARCH_URL'))
es_index = app.config.get('ELASTICSEARCH_INDEX', 'newsclipse')

assets.register('css', Bundle('style/app.less',
                              filters='less',
                              output='assets/style.css'))

assets.register('js', Bundle("vendor/underscore/underscore.js",
                            "vendor/backbone/backbone.js",
                            "vendor/modernizr/modernizr.js",
                            "js/app.js",
                             #filters='uglifyjs',
                             output='assets/app.js'))
