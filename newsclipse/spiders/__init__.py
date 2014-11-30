import logging

from newsclipse.spiders.openduka import OpenDuka
from newsclipse.spiders.wiki import Wikipedia
from newsclipse.spiders.opencorp import OpenCorporates
from newsclipse.db import save_card

log = logging.getLogger(__name__)
SPIDERS = [OpenDuka, OpenCorporates, Wikipedia]


def lookup(story, card):
    entity_type = card.get('type')
    spider_status = card.get('spider_status', {})

    for cls in SPIDERS:
        name = cls.__name__
        if spider_status.get(name) == 'done':
            continue
        try:
            spider = cls()
            if entity_type == "Person":
                card = spider.search_person(story, card)
            elif entity_type == "Company":
                card = spider.search_company(story, card)
            elif entity_type == "Organization":
                card = spider.search_organization(story, card)
            else:
                card = spider.search_generic(story, card)

            spider_status[name] = 'done'
        except Exception, e:
            log.exception(e)
            spider_status[name] = 'fail'

    card['spider_status'] = spider_status
    save_card(story, card, lookup=False)
