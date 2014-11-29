import requests
#from pprint import pprint

from newsclipse.core import calais_key


def extract_entities(text):
    URL = 'http://api.opencalais.com/tag/rs/enrich'
    headers = {
        'x-calais-licenseID': calais_key,
        'content-type': 'text/raw',
        'accept': 'application/json'
    }
    res = requests.post(URL, headers=headers,
                        data=text.encode('utf-8'))
    data = res.json()
    for k, v in data.items():
        if v.get('_type') in ['Person', 'Organization', 'Company']:
            yield {
                'title': v.get('name'),
                'offset': v.get('instances', [{}])[0].get('offset'),
                'card': 'entity',
                'type': v.get('_type')
            }

