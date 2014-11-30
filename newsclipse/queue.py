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
