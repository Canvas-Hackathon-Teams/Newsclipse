import logging

from newsclipse.core import celery as app

log = logging.getLogger(__name__)


@app.task
def extract(story_id):
    pass

    
@app.task
def lookup(story_id, entity_name, entity_type):
    pass

    #Here you add code, don't forget
    #A switch case with types (what types)
    #that returns a list of different card objects
