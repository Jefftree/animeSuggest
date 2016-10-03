from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from pymongo import MongoClient
client = MongoClient().animeList

recommendationsPath = u'/userrecs'

def cleanURL(url):
    component = url.split('/')
    component[len(component)-1] = quote(component[len(component)-1])
    return '/'.join(component)

def parseAnime(url):
    cleanedURL = cleanURL(url)
    with urllib.request.urlopen(cleanedURL + recommendationsPath) as url:
        s = url.read()
        soup = BeautifulSoup(s, "html.parser")

        aniName = soup.find('span', {'itemprop': 'name'}).text
        # if (client.animeList.find({'name': aniName}).count() > 0): return

        aniImg = soup.find('img', {'class': 'ac'})['src']

        stats = soup.find('div', {'itemprop': 'aggregateRating'})
        rating = stats.find('span', {'itemprop': 'ratingValue'}).text
        suggestions = soup.findAll('div', {'class': 'borderClass', 'style': None})
        rec = []
        for suggestion in suggestions:
            ani = suggestion.find('div', {
                'style': 'margin-bottom: 2px;'
                }).strong.text

            additionalRec = suggestion.find('a', {
                'class': 'js-similar-recommendations-button'
                })
            totalRec = 1
            if additionalRec: totalRec = totalRec + int(additionalRec.strong.text)
            graph = {
                    'name': ani,
                    'count': totalRec
                    }
            rec.append(graph)

        anime = {
            'name': aniName,
            'img': aniImg,
            'url': cleanedURL,
            'rating': rating,
            'recommendations': rec
            }

        client.animeList.insert_one(anime)
        print("Added " + aniName)

