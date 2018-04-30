from wikidata.client import Client
from pywikibot.data import api
import pywikibot
import pprint
import os
import sys

#entity_file = open(sys.argv[1], 'r')
#entities = entity_file.read().split('\n')

def getItems(site, itemtitle):
     params = { 'action' :'wbsearchentities' , 'format' : 'json' , 'language' : 'en', 'type' : 'item', 'search': itemtitle}
     request = api.Request(site=site,**params)
     return request.submit()

def getItem(site, wdItem, token):
    request = api.Request(site=site,
                          action='wbgetentities',
                          format='json',
                          ids=wdItem)    
    return request.submit()

def prettyPrint(variable):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(variable)

def getFirstID(site, entity):
    wikidataEntry = getItems(site, entity)['search'][0]
    #prettyPrint(wikidataEntry)
    return wikidataEntry['title']

def getInstanceOf(an_id):
    client = Client()
    entity = client.get(an_id, load=True)
    #loc = entity.attributes['claims']#['P1552']
    #prettyPrint(loc)
    return entity.attributes['claims']['P31'][0]['mainsnak']['datavalue']['value']['id']

def getHigherClass(the_id):
    client = Client()
    entity = client.get(the_id, load=True)
    #prettyPrint(entity.attributes['claims']['P279'][0]['mainsnak']['datavalue']['value']['id'])
    return entity.attributes['claims']['P279'][0]['mainsnak']['datavalue']['value']['id']

def climbToFindCat(the_id):
    if the_id == 'Q5':
        return 'Person'
    #elif entity.attributes['claims']['P1552'][0]['mainsnak']['datavalue']['value']['id'] == 'Q17334923':
    #    print('Location')
    else:
        a = getHigherClass(the_id)
        if a == 'Q223557':
            return 'Location'
        elif a == 'Q24229398':
            return 'Organization'
        else:
            try:
                return climbToFindCat(a)
            except:
                return "Unknown"

# Login to wikidata
def wiki_d_login():
    site = pywikibot.Site("wikidata", "wikidata")
    return site

def check_Entity(ent=str()):
    if ent != '':
        the_id = getFirstID(site, ent)
        a = getInstanceOf(the_id)
        return climbToFindCat(a)

site = wiki_d_login()
print(check_Entity('NBC'))

'''
site = wiki_d_login()
for ent in entities:
    if ent != '':
        the_id = getFirstID(site, ent)
        a = getInstanceOf(the_id)
        result = climbToFindCat(a)
        print(result)
'''

#print(entities)
#wikidataEntries = getItems(site, werd)
# Print the different Wikidata entries to the screen
#prettyPrint(wikidataEntries)

# Print each wikidata entry as an object
#for wdEntry in wikidataEntries["search"]:
#   prettyPrint(getItem(site, wdEntry["id"], token))
