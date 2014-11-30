

class Spider(object):

    def search_generic(self, story, card):
        return self.search_all(story, card)

    def search_person(self, story, card):
        return self.search_all(story, card)

    def search_company(self, story, card):
        return self.search_all(story, card)

    def search_organization(self, story, card):
        return self.search_all(story, card)

    def search_all(self, story, card):
        return card
