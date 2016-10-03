from bs4 import BeautifulSoup
import urllib.request
from pymongo import MongoClient
client = MongoClient().animeList

base_url = "https://myanimelist.net/anime/11757/Sword_Art_Online"
recommendationsPath = '/userrecs'

def parseAnime(url):
    with urllib.request.urlopen(base_url + recommendationsPath) as url:
        s = url.read()
        soup = BeautifulSoup(s, "html.parser")

        aniName = soup.find('span', {'itemprop': 'name'}).text
        if (client.animeList.find({'name': aniName}).count() > 0): return

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
            'url': base_url,
            'rating': rating,
            'recommendations': rec
            }

        client.animeList.insert_one(anime)
