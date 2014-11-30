import requests
from pprint import pprint

from newsclipse.db import save_evidence
from newsclipse.spiders.util import Spider, text_score

URL = "http://www.openduka.org/index.php/"
API_KEY = '86a6b32f398fe7b3e0a7e13c96b4f032'


class OpenDuka(Spider):

    def make_evidence(self, card, id, score, type_, record):
        #print record.keys()
        label = record.get('Citation',
                           record.get('title',
                                      record.get('Name')))
        evidence = {
            'citation': '%s: %s' % (type_, label),
            'url': URL + 'homes/tree/%s' % id,
            'source': 'OpenDuka',
            'score': score,
            'source_url': 'http://openduka.org'
        }
        save_evidence(card, evidence)
    
    def search_all(self, story, card):
        args = {'key': API_KEY, 'term': card.get('title')}
        r = requests.get(URL + "api/search", params=args)
        for match in r.json():
            score = text_score(match.get('Name'), card.get('aliases'))
            if score < 50:
                continue
            args = {'key': API_KEY, 'id': match.get('ID')}
            r = requests.get(URL + "api/entity", params=args)
            for type_set in r.json().get('data'):
                for data in type_set['dataset_type']:
                    for type_, ds in data.items():
                        for item in ds:
                            for record in item.get('dataset'):
                                self.make_evidence(card, match.get('ID'),
                                                   score, type_, record)
        return card
