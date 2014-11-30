# OpenCorporates
#
# http://api.opencorporates.com/documentation/API-Reference
#
#from pprint import pprint
from itertools import count
from newsclipse.db import save_evidence
from newsclipse.spiders.util import Spider, text_score
from urlparse import urljoin
import requests

API_HOST = 'https://api.opencorporates.com/'
CORP_ID = 'https://opencorporates.com/companies/'
API_TOKEN = 'Y2t6PVBfvoJTxhsI0ZJf'


def opencorporates_get(path, query):
    url = path if path.startswith('http:') or path.startswith('https:') else urljoin(API_HOST, path)
    params = {'per_page': 200}
    if API_TOKEN is not None:
        params['api_token'] = API_TOKEN
    params.update(query)
    res = requests.get(url, params=params)
    return res.json()


def opencorporates_paginate(path, collection_name, item_name, query):
    res = {}
    for i in count(1):
        if i > res.get('total_pages', 10000):
            return
        res = opencorporates_get(path, query)
        if 'error' in res:
            return
        res = res.get('results', {})
        for data in res.get(collection_name, []):
            data = data.get(item_name)
            yield data


class OpenCorporates(Spider):

    def make_api_url(self, url):
        if '://api.' not in url:
            url = url.replace('://', '://api.')
        return url

    def make_evidence(self, card, score, url, citation):
        evidence = {
            'citation': citation,
            'url': url,
            'source': 'OpenCorporates',
            'score': score,
            'source_url': 'https://opencorporates.com'
        }
        save_evidence(card, evidence)

    def search_organization(self, story, card):
        return self.search_company(story, card)

    def search_company(self, story, card):
        query = {'q': card.get('title')}
        for company in opencorporates_paginate('companies/search', 'companies',
                                               'company', query):
            url = company.get('opencorporates_url')
            score = text_score(company.get('name'), card.get('aliases'))
            if score < 70:
                break

            citation = 'Company record: %s' % company.get('name')
            self.make_evidence(card, score, url, citation)
        return self.search_person(story, card)

    def search_person(self, story, card):
        query = {'q': card.get('title')}
        for officer in opencorporates_paginate('officers/search', 'officers',
                                               'officer', query):
            url = officer.get('opencorporates_url')
            score = text_score(officer.get('name'), card.get('aliases'))
            if score < 70:
                break

            corp_data = officer.get('company')
            citation = '%s is %s of %s' % (officer.get('name'),
                                           corp_data.get('position'),
                                           corp_data.get('name'))
            self.make_evidence(card, score, url, citation)
        return card
