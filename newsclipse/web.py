import os
from flask import render_template, request
from datetime import datetime
from pymongo import ASCENDING

from newsclipse.core import app
from newsclipse.db import reset_db
from newsclipse.db import stories, get_story, cards
from newsclipse.db import save_card, get_card
from newsclipse.db import get_evidences
from newsclipse.util import obj_or_404, jsonify
from newsclipse.queue import extract


def angular_templates():
    partials_dir = os.path.join(app.static_folder, 'templates')
    for (root, dirs, files) in os.walk(partials_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as fh:
                file_name = file_path[len(partials_dir) + 1:]
                yield (file_name, fh.read().decode('utf-8'))


@app.route('/')
def home():
    return render_template("index.html", templates=angular_templates())


@app.route('/api/nuke', methods=['POST', 'PUT'])
def reset():
    reset_db()
    return jsonify({'status': 'ok', 'message': 'Nuked all the things'})


@app.route('/api/stories', methods=['GET'])
def stories_index():
    cur = stories.find({'$where': 'this.title.length > 1'})
    return jsonify(cur)


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
    cards_ = []
    for card in cur:
        card['evidences'] = get_evidences(card)
        cards_.append(card)
    return jsonify(cards_)


@app.route('/api/stories/<story_id>/cards', methods=['POST', 'PUT'])
def cards_create(story_id):
    story = get_story(story_id)
    card = dict(request.json)
    card.pop('_id', None)
    card.pop('evidences', None)
    card = save_card(story, card)
    return cards_get(story_id, unicode(card['_id']))


@app.route('/api/stories/<story_id>/cards/<card_id>', methods=['GET'])
def cards_get(story_id, card_id):
    story = get_story(story_id)
    card = get_card(story, card_id)
    card['evidences'] = get_evidences(card)
    return jsonify(card)


@app.route('/api/stories/<story_id>/cards/<card_id>', methods=['POST', 'PUT'])
def cards_update(story_id, card_id):
    story = get_story(story_id)
    card = obj_or_404(get_card(story, card_id))
    data = dict(request.json)
    data.pop('evidences', None)
    data['_id'] = card['_id']
    card = save_card(story, data)
    return cards_get(story_id, card_id)


