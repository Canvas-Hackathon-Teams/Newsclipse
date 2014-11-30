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
    q = {'_id': id, 'stories': story['_id']}
    return obj_or_404(cards.find_one(q))


def save_card(story, card, aliases=False):
    data = {
        'status': 'pending',
        'card': 'event',
        'aliases': [card.get('title')],
        'stories': [story['_id']],
        'created_at': datetime.utcnow(),
        'offset': 0,
    }
    data.update(card)
    data['updated_at'] = datetime.utcnow()
    q = {'stories': story['_id']}
    if aliases:
        q['aliases'] = data.get('title')
    else:
        q['_id'] = data.get('_id')

    old = cards.find_one(q)
    if old is not None:
        data['stories'] = set(old.get('stories') + [story['_id']])
        data['aliases'] = set(old.get('aliases') + data.get('aliases'))
        cards.update(q, {'$set': data})
    else:
        cards.insert(data)

    card = cards.find_one(q)
    op = {'$addToSet': {'cards': card['_id']}}
    stories.update({'_id': story['_id']}, op)
    
    from newsclipse.queue import lookup
    lookup.delay(unicode(story['_id']), unicode(card['_id']))
    return card
