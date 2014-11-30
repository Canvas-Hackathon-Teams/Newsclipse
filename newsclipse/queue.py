import logging

from newsclipse.core import celery as app
from newsclipse.extract import extract_entities
from newsclipse.db import get_story, get_card, save_card
from newsclipse import spiders

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
    spiders.lookup(story, card)
