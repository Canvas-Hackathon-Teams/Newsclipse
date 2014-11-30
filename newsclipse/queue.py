import logging

from newsclipse.core import celery as app
from newsclipse.extract import extract_entities
from newsclipse.db import get_story, save_card

log = logging.getLogger(__name__)


@app.task
def extract(story_id):
    story = get_story(story_id)
    for card in extract_entities(story.get('text')):
        save_card(story, card, key='title')

<<<<<<< HEAD
	
@app.task
def lookup(story_id, entity_name, entity_type):
=======

def lookup(story_id, card_id):
>>>>>>> db4f9374cf91247bad0fb867ef2aa7ecd588863d

	#Here you add code, don't forget
	#that returns a list of different card objects

	if entity_type is "person":
			#run which lookup services
			pass
	elif entity_type is "places":
			#run which lookup services
			pass
	elif entity_type is "social tags":
			#run which lookup services
			pass
	elif entity_type is "companies":
			#run which lookup services
			pass
	elif entity_type is "organisations":
			#run which lookup services
			pass
	
	#title
	#text
	#picture (in case of person)
	#
