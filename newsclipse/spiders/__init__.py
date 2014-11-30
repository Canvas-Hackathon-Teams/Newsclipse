from newsclipse.spiders.openduka import OpenDuka
from newsclipse.db import save_card

SPIDERS = [OpenDuka]


def lookup(story, card):
    entity_type = card.get('type')
    for cls in SPIDERS:
        spider = cls()
        if entity_type == "Person":
            card = spider.search_person(story, card)
        elif entity_type == "Company":
            card = spider.search_company(story, card)
        elif entity_type == "Organization":
            card = spider.search_organization(story, card)
        else:
            card = spider.search_generic(story, card)

    save_card(story, card, lookup=False)
