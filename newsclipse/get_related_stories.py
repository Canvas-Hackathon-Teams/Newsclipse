#from BeautifulSoup import BeautifulSoup
import re
import urllib


def get_related(entities):
    all_entities = []
    tags = []
    for e in entities:
        if e['card'] == 'entity':
            all_entities.append(e)
        else:
            tags.append(e)

    tags.sort(key=lambda x: -x['relevance'])
    all_entities.sort(key=lambda x: -x['relevance'])

    all_titles = set()
    for entity in all_entities:
        t = entity['title']
        all_titles.add(t)
        for t in entity['aliases']:
            all_titles.add(t)

    entities = set()

    def is_subset(title1, title2):

        count = 0
        for word in title1.split(' '):
            if len(word)>2:
                if word in title2:
                    count += 1
                    if count ==2:
                        return True
        else:
            return False

    def add_entity(title, relevance):
        for entity in entities:
            etitle = entity[0]
            if is_subset(title, etitle) or is_subset(etitle, title):
                if len(entity) < len(title):
                    return
                else:
                    entities.remove(entity)
                    entities.add((title, relevance))
        else:
            entities.add((title, relevance))

    for entity in all_entities:
        aliases = entity['aliases']
        aliases.sort(key=lambda x: -len(x))
        if aliases:
            best_title = aliases[0]
        else:
            best_title = entity['title']
        add_entity(best_title, entity['relevance'])

    lentities = list(entities)
    lentities.sort(key= lambda x: -x[1])
    lentities = [lentity[0] for lentity in lentities[:5]]


    def is_not_subset_of_any(x, entities):
        for entity in entities:
            if is_subset(x, entity):
                return False
        return True


    tag_titles = [e['title'] for e in tags]
    relevant_tags = filter(lambda x:is_not_subset_of_any(x, lentities), tag_titles)

    def get_articles():
        results = []
        link_set = set()
        m = 0
        for i in range(0, len(lentities)):
            for j in range(i+1, len(lentities)):
                for tag in relevant_tags:
                    e1 = lentities[i]
                    e2 = lentities[j]
                    text = e1 + e2 + tag

                    site = urllib.urlopen('http://duckduckgo.com/html/?q=%s' % text)
                    data = site.read()
                    parsed = BeautifulSoup(data)
                    #
                    # = [link.a['href'] for link in parsed.findAll('div', {'class': re.compile('links_main*')})][:4]
                    parsed = parsed.findAll('div', {'class': re.compile('links_main*')})
                    if parsed[0].span:
                        if parsed[0].span.text == "No results.":
                            continue
                    for k, p in enumerate(parsed):
                        link = p.a['href']
                        if link in link_set:
                            continue
                        link_set.add(link)
                        k+=1
                        if k==3:
                            break
                        d = p.div
                        innerhtml = "".join([str(x) for x in d.contents])
                        content = innerhtml.replace('<b>', '').replace('</b>', '')
                        results.append((link, content))
                        m+=1
                        if m==10:
                            return results

    return get_articles()
