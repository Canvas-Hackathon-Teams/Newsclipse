import logging
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from newsclipse.core import assets
from newsclipse.web import app
from newsclipse.search import init_elasticsearch
from newsclipse.search import reset_elasticsearch

log = logging.getLogger(__name__)
init_elasticsearch()
manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


@manager.command
def reset():
    """ Destroy the current database and create a new one. """
    reset()

if __name__ == "__main__":
    manager.run()
