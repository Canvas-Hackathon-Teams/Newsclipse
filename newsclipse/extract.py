import requests

from newsclipse.core import calais_key


TAGS = {
    'entity': ['Person', 'Organization', 'Company'],
    #'location': ['Country', 'Region', 'City', 'ProvinceOrState',
    #             'Continent', 'NaturalFeature', 'Facility']
}


def extract_entities(text):
    URL = 'http://api.opencalais.com/tag/rs/enrich'
    headers = {
        'x-calais-licenseID': calais_key,
        'content-type': 'text/raw',
        'accept': 'application/json'
    }
    res = requests.post(URL, headers=headers,
                        data=text.encode('utf-8'))
    result = res.json()
    
    sections = []
    for k, v in result.items():
        if '_type' not in v:
            continue
        
        tag = None
        for tag_, types in TAGS.items():
            if v.get('_type') in types:
                tag = tag_

        if tag is None:
            continue

        for instance in v.get('instances'):
            instance.update({
                'label': v.get('name'),
                'type': v.get('_type'),
                'tag': tag
            })
            sections.append(instance)

    print sections