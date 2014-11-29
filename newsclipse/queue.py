import logging

from newsclipse.core import celery as app
from newsclipse.extract import extract_entities

log = logging.getLogger(__name__)


@app.task
def extract(story_id):
    test = "Vladimir Putin is giving Angela Merkel a big fat wet kiss!"
    entities = extract_entities(test)

    
@app.task
def lookup(story_id, entity_name, entity_type):
    pass

    #Here you add code, don't forget
    #A switch case with types (what types)
    #that returns a list of different card objects
