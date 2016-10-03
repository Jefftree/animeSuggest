from bs4 import BeautifulSoup
import urllib.request

class AnimeDB:
    base_url = "http://myanimelist.net/recommendations.php?s=recentrecs&t=anime"

    def __init__(self, pages):
        self.mapping = []
        self.pages = pages
        self.recommender = {}
        self.CrawlMAL()
        self.genRecommender()

    def CrawlMAL(self):
        prefix = '&show='
        for x in range(self.pages):
            self.addToDB(self.base_url + prefix + str(x * 100))

    def getDom(self, uri):
        with urllib.request.urlopen(uri) as url:
            s = url.read()
        soup = BeautifulSoup(s, "html.parser")
        blob = soup.findAll('div', {'class': 'spaceit', 'class': 'borderClass'})
        return blob

    def addToDB(self, url):
        blob = self.getDom(url)
        for chunk in blob:
            self.mapping.append(self.parse_links(chunk))

    def parse_links(self, chunk):
        unit = chunk.findAll('a', {'class': ''})
        ifthen = {}
        ifthen['if'] = unit[0].strong.contents[0]
        ifthen['then'] = unit[2].strong.contents[0]
        return ifthen

    def genRecommender(self):
        for x in self.mapping:
            if x['if'] in self.recommender:
                if x['then'] in self.recommender[x['if']]:
                    self.recommender[x['if']][x['then']] += 1
                else:
                    self.recommender[x['if']][x['then']] = 1

            else:
                self.recommender[x['if']] = {x['then'] : 1}

    def printRecList(self):
        for anime in adb.recommender:
            print(anime + ': '  + str(adb.recommender[x]))

    def recAnime(self, anime):
        if anime in adb.recommender:
            print(adb.recommender[anime])
        else:
            print('Anime not found')

    def recList(self, animeList):
        newList = {}
        for anime in animeList:
            if anime in self.recommender:
                oldList = self.recommender[anime]
                for recAnime in oldList:
                    if recAnime in newList:
                        newList[recAnime] += oldList[recAnime]
                    else:
                        newList[recAnime] = oldList[recAnime]
            else:
                print('Anime: ' + anime + ' not found')
        print(newList)

adb = AnimeDB(10)

adb.recAnime('Sword Art Online')

adb.recList(['Shinsekai yori', 'Shingeki no Kyojin', 'No Game No Life'])

