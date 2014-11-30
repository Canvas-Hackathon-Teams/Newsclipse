import logging

from newsclipse.spiders.openduka import OpenDuka
from newsclipse.db import save_card

log = logging.getLogger(__name__)
SPIDERS = [OpenDuka]


def lookup(story, card):
    entity_type = card.get('type')
    for cls in SPIDERS:
        #log.warn("CLS" + repr(cls))
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

    save_card(story, card, lookup=False)
