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


def lookup(story_id, card_id):

	#Here you add code, don't forget
	#that returns a list of different card objects
	switch(n) {
		case "person":
			#run which lookup services
			break;
		case "places":
			#run which lookup services
			break;
		case "social tags":
			#run which lookup services
			break;
		case "companies":
			#run which lookup services
			break;
		case "organisations":
			#run which lookup services
			break;
	}
	
	#title
	#text
	#picture (in case of person)
	#
