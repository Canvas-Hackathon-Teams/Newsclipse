import logging
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from newsclipse.core import assets
from newsclipse.web import app

log = logging.getLogger(__name__)
manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


#@manager.command
#def initdb():
#    """ Destroy the current database and create a new one. """
#    initdb_()
#    init_elasticsearch()

if __name__ == "__main__":
    manager.run()
