import logging
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from newsclipse.core import assets
from newsclipse.web import app
from newsclipse.db import reset_db

log = logging.getLogger(__name__)
manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


@manager.command
def reset():
    """ Destroy the current database and create a new one. """
    reset_db()

if __name__ == "__main__":
    manager.run()
