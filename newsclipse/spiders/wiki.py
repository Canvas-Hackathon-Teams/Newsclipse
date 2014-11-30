import requests
import wikipedia


from newsclipse.db import save_evidence
from newsclipse.spiders.util import Spider, text_score


class Wikipedia(Spider):
    
    def search_all(self, story, card):
        try:
            #TODO: have a word score to check the right page
            #TODO: errors are still shown, So try is not the way
            text = wikipedia.summary(card.get('title'))
            #Add wiki text to card
            card['wikiText'] = text
        except ValueError:
            pass

        return card
