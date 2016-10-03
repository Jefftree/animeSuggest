from pymongo import MongoClient
from collections import Counter
from functools import reduce

client = MongoClient().animeList
AnimeList = client.animeList

############ HELPERS ###############

def mergeAniRec(rec1, rec2):
    rec1 = Counter(rec1)
    rec2 = Counter(rec2)
    return rec1 + rec2

def toKeyVal(arr):
    aniDict = {}
    for kvp in arr:
        aniDict[kvp['name']] = kvp['count']
    return aniDict

######## EXPORTS ###################

def getGroupRec(aniList):
    recList = map(getRec, aniList)
    recList = dict(reduce(mergeAniRec, recList))
    print(recList)

def getRec(anime):
    result = AnimeList.find({'name': anime})
    if result.count() > 0:
        anime = result[0]
        recommendations = anime['recommendations']
        return toKeyVal(recommendations[:5])
    else:
        print("ERROR: " + anime + " not in crawl list")
        return []

getGroupRec(['Clannad: After Story', 'Angel Beats!'])
