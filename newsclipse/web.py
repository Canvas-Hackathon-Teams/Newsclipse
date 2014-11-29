from flask import render_template, request
from bson.objectid import ObjectId
#from restpager import Pager

from newsclipse.core import app
from newsclipse.db import db, stories
from newsclipse.util import obj_or_404, jsonify
from newsclipse.queue import extract, lookup


@app.route('/')
def home():
    extract.delay('huhu')
    #pager = Pager(search_block(q))
    return render_template("index.html")


@app.route('/api/stories', methods=['GET'])
def stories_index():
    return jsonify(stories.find())


@app.route('/api/stories', methods=['POST', 'PUT'])
def stories_create():
    story = request.json
    ret = stories.insert(story)
    return jsonify(stories.find_one({'_id': ret}))


@app.route('/api/stories/<id>', methods=['GET'])
def stories_get(id):
    id = ObjectId(id)
    story = obj_or_404(stories.find_one({'_id': id}))
    return jsonify(story)


@app.route('/api/stories/<id>', methods=['POST', 'PUT'])
def stories_update(id):
    id = ObjectId(id)
    story = obj_or_404(stories.find_one({'_id': id}))
    stories.update({'_id': id}, {'$set': request.json})
    story = obj_or_404(stories.find_one({'_id': id}))
    return jsonify(story)

