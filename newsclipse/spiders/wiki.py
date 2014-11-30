import logging
import wikipedia

from newsclipse.spiders.util import Spider


log = logging.getLogger(__name__)


class Wikipedia(Spider):
    
    def search_all(self, story, card):
        try:
            #TODO: have a word score to check the right page
            #TODO: errors are still shown, So try is not the way
            text = wikipedia.summary(card.get('title'))
            #Add wiki text to card
            card['wiki_text'] = text
        except wikipedia.WikipediaException, pe:
            log.exception(pe)

        return card
