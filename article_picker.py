import json
from collections import OrderedDict

year = 2017

while True:
    # yes, reload these every iteration
    articles = json.load(open('./articles.json', 'r'), object_pairs_hook=OrderedDict)
    processed = json.load(open('./articles_processed.json', 'r'))
    unreplicable = json.load(open('./articles_unreplicable.json', 'r'))
    ignore = json.load(open('./articles_ignore.json', 'r'))

    # return an unprocessed article url
    def pick_article(year):
        for article in articles[str(year)].keys():
            if article not in processed[str(year)].keys() \
                    and article not in unreplicable \
                    and article not in ignore:
                return article

    article_key = pick_article(year)
    article_json = articles[str(year)][article_key]

    print()
    print(article_key)
    print(json.dumps(article_json))
    print(article_json['attributes']['full_text'])

    response = input("P (processed), U (unreplicable), I (ignore) | ")
    if response.lower() == 'u':
        unreplicable.append(article_key)
        with open('./articles_unreplicable.json', 'w') as file:
            file.write(json.dumps(unreplicable))
