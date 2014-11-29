import logging
from pyelasticsearch.exceptions import ElasticHttpNotFoundError
from pyelasticsearch.exceptions import IndexAlreadyExistsError

from newsclipse.core import es, es_index
#from newsclipse.util import AppEncoder

log = logging.getLogger(__name__)


class ESResultProxy(object):
    """ This is required for the pager to work. """

    def __init__(self, doc_type, query):
        self.doc_type = doc_type
        self.query = query
        self._limit = 10
        self._offset = 0

    def limit(self, num):
        self._limit = num
        return self

    def offset(self, num):
        self._offset = num
        return self

    @property
    def result(self):
        if not hasattr(self, '_result'):
            q = self.query.copy()
            q['from'] = self._offset
            q['size'] = self._limit
            self._result = es.search(index=es_index,
                                     doc_type=self.doc_type,
                                     query=q)
        return self._result

    def __len__(self):
        return self.result.get('hits', {}).get('total')

    def __iter__(self):
        for hit in self.result.get('hits', {}).get('hits', []):
            res = hit.get('_source')
            res['score'] = hit.get('_score')
            yield res


def init_elasticsearch():
    try:
        es.create_index(es_index)
        log.info("Creating ElasticSearch index and uploading mapping...")
    except IndexAlreadyExistsError:
        pass
    #es.put_mapping(es_index, Block.doc_type, {Block.doc_type: BLOCK_MAPPING})


def reset_elasticsearch():
    try:
        es.delete_index(es_index)
    except ElasticHttpNotFoundError:
        pass
    init_elasticsearch()


#def index_block(block):
#    es.json_encoder = AppEncoder
#    es.index(es_index, Block.doc_type, block)


def search(doc_type, query):
    return ESResultProxy(doc_type, query)
