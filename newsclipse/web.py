from flask import render_template, request
from bson.objectid import ObjectId
#from restpager import Pager

from newsclipse.core import app
from newsclipse.db import stories, get_story, cards
from newsclipse.db import save_card, get_card
from newsclipse.util import obj_or_404, jsonify
from newsclipse.queue import extract, lookup


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api/stories', methods=['GET'])
def stories_index():
    return jsonify(stories.find())


@app.route('/api/stories', methods=['POST', 'PUT'])
def stories_create():
    story = dict(request.json)
    story.pop('_id', None)
    story['cards'] = []
    ret = stories.insert(story)
    extract.delay(unicode(ret))
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
    stories.update({'_id': story['_id']}, {'$set': data})
    extract.delay(id)
    return jsonify(get_story(id))


@app.route('/api/stories/<story_id>/cards', methods=['GET'])
def cards_index(story_id):
    story = get_story(story_id)
    return jsonify(cards.find({'story_id': story['_id']}))


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


