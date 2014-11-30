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
    
    if entity_type == "Person":
        #run which lookup services
        #run trough OpenDuka
        checkDuka(card)
	
    elif entity_type == "Company":
        #run which lookup services
        #run trough OpenDuka
        checkDuka(card)

    elif entity_type == "Organization":
		#run which lookup services
		#run trough OpenDuka? probably not
        checkDuka(card)

    save_card(story,card,lookup=False)

def checkDuka(card):
	if 'duka_results' not in card:
		results = openDukaLookup(card.get('title'))
		if results is not False:
			card['duka_results'] = results
