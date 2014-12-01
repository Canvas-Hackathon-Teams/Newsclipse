from bson.objectid import ObjectId
from pymongo import DESCENDING
from datetime import datetime

from newsclipse.core import db
from newsclipse.util import obj_or_404

stories = db['stories']
cards = db['cards']
evidences = db['evidences']


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


def save_card(story, card, aliases=False, lookup=True):
    data = {
        'status': 'pending',
        'card': 'event',
        'evidences': [],
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
        data['stories'] = list(set(old.get('stories') + [story['_id']]))
        data['aliases'] = list(set(old.get('aliases') + data.get('aliases')))
        data['evidences'] = old.get('evidences')
        cards.update(q, {'$set': data})
    else:
        q['_id'] = cards.insert(data)

    card = cards.find_one(q)
    op = {'$addToSet': {'cards': card['_id']}}
    stories.update({'_id': story['_id']}, op)

    if lookup:
        from newsclipse.queue import lookup_all
        lookup_all(unicode(story['_id']), unicode(card['_id']))

    return card


def save_evidence(card, evidence):
    q = {'url': evidence.get('url')}
    existing = evidences.find_one(q)
    if existing is None:
        evidence['created_at'] = datetime.utcnow()
        evidence['cards'] = [card['_id']]
    else:
        evidence['cards'] = list(set(existing['cards'] + [card['_id']]))
    evidence['updated_at'] = datetime.utcnow()
    evidence['score'] = evidence.get('score') or 0
    evidences.update(q, evidence, upsert=True)
    evidence = evidences.find_one(q)
    op = {'$addToSet': {'evidences': evidence['_id']}}
    cards.update({'_id': card['_id']}, op)
    return evidence


def get_evidences(card):
    q = {'cards': card['_id']}
    return evidences.find(q).sort('score', DESCENDING)
