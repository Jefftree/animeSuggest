from pymongo import MongoClient
from collections import Counter
from functools import reduce
from userSearch import getUserAnime
from logger import logger
import pprint

pp = pprint.PrettyPrinter(indent=4)

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
    return recList

def getRec(anime):
    result = AnimeList.find({'name': anime})
    if result.count() > 0:
        anime = result[0]
        recommendations = anime['recommendations']
        return toKeyVal(recommendations[::])
    else:
        logger.debug(anime + " not in crawl list")
        return []

aniList = map(lambda ani: ani['name'], getUserAnime('jefftree'))
aniRec = getGroupRec(aniList).items()
aniRec = sorted(aniRec, key=lambda ani: ani[1], reverse=True)
pp.pprint(aniRec[:50]) # Top 50 for now
