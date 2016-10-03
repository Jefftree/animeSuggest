from bs4 import BeautifulSoup
import urllib.request
from parseAnime import parseAnime

def extractAnimeURL(ani):
    return (ani.find('div', {
            'class': 'detail'
            }).find('a', {'class': 'hoverinfo_trigger' })['href'])

def extractPage(num):
    NUM_PER_PAGE = 50
    base_url = "https://myanimelist.net/topanime.php"
    pagePath = '?limit=' + str(num * NUM_PER_PAGE)

    with urllib.request.urlopen(base_url + pagePath) as url:
        s = url.read()
        soup = BeautifulSoup(s, "html.parser")

        queue = []

        animeList = soup.findAll('tr', {'class': 'ranking-list'})
        animeList = map(extractAnimeURL, animeList)
        queue.extend(animeList)
        for anime in queue:
            parseAnime(anime)

    print("Processed Batch #" + str(num))

for i in range(10):
    extractPage(i)
