from bson.objectid import ObjectId

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
