import logging

from newsclipse.spiders.openduka import OpenDuka
from newsclipse.spiders.wiki import Wikipedia
from newsclipse.spiders.opencorp import OpenCorporates
from newsclipse.db import save_card, get_card

log = logging.getLogger(__name__)

SPIDERS = {
    'OpenDuka': OpenDuka,
    'OpenCorporates': OpenCorporates,
    'Wikipedia': Wikipedia
}


def lookup(story, card, spider_name):
    entity_type = card.get('type')
    spider_status = card.get('spider_status', {})

    cls = SPIDERS.get(spider_name)
    if spider_status.get(spider_name) == 'done':
        return

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
    except Exception, e:
        log.exception(e)

    ncard = get_card(story, unicode(card['_id']))
    spider_status = ncard.get('spider_status', {})
    spider_status[spider_name] = 'done'
    card['spider_status'] = spider_status
    save_card(story, card, lookup=False)
