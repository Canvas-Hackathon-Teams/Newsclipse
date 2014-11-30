import logging

from newsclipse.core import celery as app
from newsclipse.extract import extract_entities
from newsclipse.db import get_story, get_card, save_card
from newsclipse.openduka import openDukaLookup

log = logging.getLogger(__name__)


@app.task
def extract(story_id):
    story = get_story(story_id)
    try:
        for card in extract_entities(story.get('text')):
            save_card(story, card, aliases=True)
    except Exception, e:
        print e


@app.task
def lookup(story_id, card_id):
    story = get_story(story_id)
    card = get_card(story, card_id)
    entity_type = card.get('type')
    
    #Here you add code, don't forget
    #that returns a list of different card objects

    if entity_type == "Person":
        #run which lookup services

        #run trough OpenDuka
        # openDukaLookup(personNAME!)
        pass
    elif entity_type == "Company":
        #run which lookup services
        #run trough OpenDuka
        pass
    elif entity_type == "Organization":
        #run which lookup services
        #run trough OpenDuka? probably not
        pass
    
    #title
    #text
    #picture (in case of person)
    #
