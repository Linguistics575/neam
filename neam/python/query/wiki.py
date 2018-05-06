"""
wiki.py

Defines an API for retrieving Wikidata entities and checking against their type
hierarchy. Employs extensive caching, so no HTTP request will ever be run more than once.

Use:
    # The wiki entry is looked up when the entity is initialized
    queen_elizabeth = Entity('Queen Elizabeth')
    queen_elizabeth.label  # 'Elizabeth II'
    queen_elizabeth.qid    # 'Q9682'

    # Entities can be initialized with their Q-IDs to bypass the wikidata lookup
    henry_viii = Entity('Q38370')
    # Entities initialized this way will not have a label
    henry_viii.label  # None

    # Checking if one entity is an instance of another:
    human = Entity('human')
    queen_elizabeth.is_a(human)     # True
    # This can be combined into one step; the lookup will be done automatically
    queen_elizabeth.is_a('human')   # True
    # False instance checks also work
    queen_elizabeth.is_a('lizard')  # False
    # Instance checks can be done with Q-IDs
    queen_elizabeth.is_a('Q5')  # True

    # Multiple relations can be checked at the same time
    queen_elizabeth.which(['person', 'place', 'thing'])  # ['person', 'thing']
    # Multiple relation checks can be done with Q-IDs
    queen_elizabeth.which(['Q5', 'Q82794', 'Q35120'])  # ['Q5', 'Q35120']
    # Multiple relation checks can be done with mixed lists
    queen_elizabeth.which(['Q5', 'place', 'thing'])  # ['Q5', 'thing']
"""
import re
import requests

import pywikibot
from pywikibot.data import api

URL = 'https://query.wikidata.org/sparql'
CACHE = {}

PYWIKI_SITE = pywikibot.Site('wikidata', 'wikidata')
PYWIKI_PARAMS = {
    'action': 'wbsearchentities', 'format': 'json', 'language': 'en', 'type': 'item'
}


class Entity:
    """
    Defines a Wiki entity
    """
    def __init__(self, label):
        """
        Initializes the entity.

        :param label: Either the label for the entity, or its Q-ID
        :type label: str
        """
        result = lookup(label) 
        self._qid = result['id']
        self._label = result['label']
        self._types = None

    @property
    def qid(self):
        """
        The ID used by Wikidata to uniquely identify the entity

        Will be None if the the entity is not in Wikidata.

        :rtype: Union[str, None]
        """
        return self._qid

    @property
    def label(self):
        """
        The human readable name of the entity

        Will be None if the entity is not in Wikidata or the object was initialized with
        a QID.

        :rtype: Union[str, None]
        """
        return self._label

    @property
    def types(self):
        """
        The QIDs of the entities this entity inherits from

        :rtype: list of str
        """
        self._get_types()
        return self._types

    def __bool__(self):
        return self._qid is not None

    def is_a(self, other):
        """
        Checks to see if this entity is an instance of or is subclassed by another
        entity.

        :param other: Either the label for an entity, its Q-ID, or an Entity object
        :type other: str or Entity
        :return: True if this entity is subclassed, and False otherwise
        """
        self._get_types()
        if isinstance(other, str):
            other = Entity(other)
        return other._qid in self._types

    def which(self, options):
        """
        Determines which of a list of items this entity is subclassed by

        :param options: The options to choose from
        :type options: list of Union[str, Entity]
        :return: The items this Entity is subclassed by
        :rtype: list of str
        """
        self._get_types()
        return [op for op in options if self.is_a(Entity(op))]

    def _get_types(self):
        """
        Caches all of the supertypes for this entity by polling Wikidata
        """
        if not self._types:
            if self:
                query = 'SELECT ?type {{ wd:{} wdt:P31/wdt:P279* ?type. }}'.format(self._qid)
                response = run_sparql_query(query)
                self._types = [row['type']['value'].split('/')[-1] for row in response]
            else:
                # If the entity is null, don't bother asking Wikidata about it
                self._types = []

    def __str__(self):
        """
        :return: The Entity's label if it has one, or its Q-ID otherwise
        """
        return self._label or self._qid


def run_sparql_query(query):
    """
    Runs a SPARQL query against Wikidata

    :param query: The query to run
    :type query: str
    :return: The result set from the query
    :rtype: varies
    """
    params = {
        'query': query,
        'format': 'json'
    }
    response = requests.get(url=URL, params=params)
    return response.json()['results']['bindings']


def lookup(string):
    """
    Looks up the entity data for some entity

    :param entity: Either the label for the entity, or its Q-ID
    :type entity: str
    :return: The entity data, consisting of its label and its Q-ID. If a Q-ID was passed
             in, the label will be None.
    :rtype: dict
    """
    if string in CACHE:
        return CACHE[string]

    if re.match('[A-Z]\d+', string):
        entity = { 'id': string, 'label': None }
    else:
        request = api.Request(site = PYWIKI_SITE, search = string, **PYWIKI_PARAMS)
        result = request.submit()['search']
        entity = result[0] if len(result) > 0 else { 'id': None, 'label': None }

    CACHE[string] = entity
    return entity

