import logging

from newsclipse.core import celery as app
from newsclipse.extract import extract_entities
from newsclipse.db import get_story, get_card, save_card

log = logging.getLogger(__name__)


@app.task
def extract(story_id):
    story = get_story(story_id)
    for card in extract_entities(story.get('text')):
        save_card(story, card, key='title')


def lookup(story_id, card_id):
    story = get_story(story_id)
    card = get_card(story, card_id)
    entity_type = card.get('type')
    
    #Here you add code, don't forget
    #that returns a list of different card objects

    if entity_type == "person":
        #run which lookup services
        pass
    elif entity_type == "places":
        #run which lookup services
        pass
    elif entity_type == "social tags":
        #run which lookup services
        pass
    elif entity_type == "companies":
        #run which lookup services
        pass
    elif entity_type == "organisations":
        #run which lookup services
        pass
    
    #title
    #text
    #picture (in case of person)
    #
