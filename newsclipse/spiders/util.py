from Levenshtein import distance

SCORE_CUTOFF = 50


def light_normalize(text):
    text = unicode(text)
    text = text.strip().lower()
    return text


def text_score(match, candidates):
    if isinstance(candidates, basestring):
        candidates = [candidates]
    match_n = light_normalize(match)
    best_score = 0
    for candidate in candidates:
        cand_n = light_normalize(candidate)
        dist = float(distance(match_n, cand_n))
        l = float(max(len(match_n), len(cand_n)))
        score = ((l - dist) / l) * 100
        best_score = max(int(score), best_score)
    return best_score


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
