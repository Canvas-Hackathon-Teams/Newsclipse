import logging

from newsclipse.core import celery as app
from newsclipse.extract import extract_entities
from newsclipse.db import get_story, get_card, save_card
from newsclipse import spiders
from newsclipse.get_related_stories import get_related, get_related_to_person

log = logging.getLogger(__name__)


@app.task
def extract(story_id):
    story = get_story(story_id)
    try:
        for card in extract_entities(story.get('text')):
            if card['card'] == 'entity':
                save_card(story, card, aliases=True)
    except Exception, e:
        log.exception(e)


@app.task
def lookup(story_id, card_id):
    try:
        story = get_story(story_id)
        card = get_card(story, card_id)
        spiders.lookup(story, card)
    except Exception, e:
        log.exception(e)

@app.task
def get_related_stories(story_id):
    story = get_story(story_id)
    try:
        entities = extract_entities(story.get('text'))
        return get_related(entities)
    except Exception, e:
        log.exception(e)

@app.task
def get_related_stories_to_person(story_id, person):
    story = get_story(story_id)
    try:
        entities = extract_entities(story.get('text'))
        return get_related_to_person(entities, person)
    except Exception, e:
        log.exception(e)