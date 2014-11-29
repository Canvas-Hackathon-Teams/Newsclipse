from newsclipse.core import db

stories = db['stories']
cards = db['cards']


def reset_db():
    for name in db.collection_names():
        if name.startswith('system.'):
            continue
        db[name].drop()
