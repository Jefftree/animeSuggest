from bs4 import BeautifulSoup
import urllib.request

def getUserAnime(user):
    url = 'https://myanimelist.net/malappinfo.php?u=' + \
    user + '&status=all&type=anime'
    with urllib.request.urlopen(url) as url:
        s = url.read()
        soup = BeautifulSoup(s, "lxml")
        aniList = soup.findAll('anime')
        personalList = []
        for anime in aniList:
            if anime.find('my_status').text != "2": continue
            aniName = anime.find('series_title').text
            aniRating = anime.find('my_score').text
            if aniRating == '0': continue

            ani = {
                'name': aniName,
                'rating': aniRating
                    }
            personalList.append(ani)
        return personalList

