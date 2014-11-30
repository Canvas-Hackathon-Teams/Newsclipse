from bson.objectid import ObjectId
from datetime import datetime

from newsclipse.core import db
from newsclipse.util import obj_or_404

stories = db['stories']
cards = db['cards']


def reset_db():
    for name in db.collection_names():
        if name.startswith('system.'):
            continue
        db[name].drop()


def get_story(id):
    if not isinstance(id, ObjectId):
        id = ObjectId(id)
    return obj_or_404(stories.find_one({'_id': id}))


def get_card(story, id):
    if not isinstance(id, ObjectId):
        id = ObjectId(id)
    q = {'_id': id, 'story_id': story['_id']}
    return obj_or_404(cards.find_one(q))


def save_card(story, card, key='_id'):
    data = {
        'status': 'pending',
        'story_id': story['_id'],
        'card': 'event',
        'created_at': datetime.utcnow(),
        'offset': 0,
    }
    data.update(card)
    data['updated_at'] = datetime.utcnow()
    q = {key: data.get(key), 'story_id': story['_id']}
    cards.update(q, {'$set': data}, upsert=True)
    card = cards.find_one(q)
    up = {'$addToSet': {'cards': card['_id']}}
    stories.update({'_id': story['_id']}, up)
    
    from newsclipse.queue import lookup
    lookup.delay(unicode(story['_id']), unicode(card['_id']))
    return card
