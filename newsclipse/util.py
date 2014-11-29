import simplejson
from datetime import datetime, date
from inspect import isgenerator

from werkzeug.exceptions import NotFound
from flask import Response, request


def obj_or_404(obj):
    if obj is None:
        raise NotFound()
    return obj


class AppEncoder(simplejson.JSONEncoder):
    """ This encoder will serialize all entities that have a to_dict
    method by calling that method and serializing the result. """

    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif isinstance(obj, datetime):
            return obj.isoformat() + 'Z'
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isgenerator(obj):
            return [o for o in obj]
        elif isinstance(obj, set):
            return [o for o in obj]
        return super(AppEncoder, self).default(obj)


def jsonify(obj, status=200, headers=None, index=False, encoder=AppEncoder):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    data = encoder().encode(obj)
    if 'callback' in request.args:
        cb = request.args.get('callback')
        data = '%s && %s(%s)' % (cb, cb, data)
    return Response(data, headers=headers,
                    status=status,
                    mimetype='application/json')
