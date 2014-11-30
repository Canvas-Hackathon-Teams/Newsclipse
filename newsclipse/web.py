from flask import render_template, request
from datetime import datetime
from pymongo import ASCENDING
#from restpager import Pager

from newsclipse.core import app
from newsclipse.db import reset_db
from newsclipse.db import stories, get_story, cards
from newsclipse.db import save_card, get_card
from newsclipse.util import obj_or_404, jsonify, AppEncoder
from newsclipse.queue import extract


@app.route('/')
def home():
    stories_ = stories.find()
    stories_ = AppEncoder().encode(stories_)
    return render_template("index.html", stories=stories_)


@app.route('/api/nuke', methods=['POST', 'PUT'])
def reset():
    reset_db()
    return jsonify({'status': 'ok', 'message': 'Nuked all the things'})


@app.route('/api/stories', methods=['GET'])
def stories_index():
    return jsonify(stories.find())


@app.route('/api/stories', methods=['POST', 'PUT'])
def stories_create():
    story = dict(request.json)
    story.pop('_id', None)
    story['cards'] = []
    story['created_at'] = datetime.utcnow()
    story['updated_at'] = datetime.utcnow()
    ret = stories.insert(story)
    # extract.delay(unicode(ret))
    extract(unicode(ret))
    return stories_get(ret)


@app.route('/api/stories/<id>', methods=['GET'])
def stories_get(id):
    return jsonify(get_story(id))


@app.route('/api/stories/<id>', methods=['POST', 'PUT'])
def stories_update(id):
    story = get_story(id)
    data = dict(request.json)
    data.pop('_id', None)
    data.pop('cards', None)
    story['updated_at'] = datetime.utcnow()
    stories.update({'_id': story['_id']}, {'$set': data})
    # extract.delay(id)
    extract(id)
    return jsonify(get_story(id))


@app.route('/api/stories/<story_id>/cards', methods=['GET'])
def cards_index(story_id):
    story = get_story(story_id)
    cur = cards.find({'stories': story['_id']})
    cur = cur.sort('offset', ASCENDING)
    return jsonify(cur)


@app.route('/api/stories/<story_id>/cards', methods=['POST', 'PUT'])
def cards_create(story_id):
    story = get_story(story_id)
    card = dict(request.json)
    card.pop('_id', None)
    return jsonify(save_card(story, card))


@app.route('/api/stories/<story_id>/cards/<card_id>', methods=['GET'])
def cards_get(story_id, card_id):
    story = get_story(story_id)
    return obj_or_404(get_card(story, card_id))


@app.route('/api/stories/<story_id>/cards/<card_id>', methods=['POST', 'PUT'])
def cards_update(story_id, card_id):
    story = get_story(story_id)
    card = obj_or_404(get_card(story, card_id))
    data = dict(request.json)
    data['_id'] = card['_id']
    return jsonify(save_card(story, data))


