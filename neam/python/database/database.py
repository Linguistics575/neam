"""
database.py

Defines the ActiveRecord model for the NEAM Database
"""
import datetime
import re
import atexit

from peewee import *

__all__ = ['Tag', 'Entity', 'Lemma', 'DB']


""" The database connection """
DB = SqliteDatabase('test_db.db')


class BaseModel(Model):
    """
    Base model for the database. Defines high level characteristics for all tables.
    """
    class Meta:

        """ The database connection to use for queries """
        database = DB


class OpenModel(BaseModel):
    """
    Superclass for models that are expected to be regularly added to
    """

    """ When the entity was added to the database """
    created_at = DateTimeField(default=datetime.datetime.now)

    """ Whether this entity is outwardly visible """
    is_published = BooleanField(default=False)


class ClosedModel(BaseModel):
    """
    Superclass for models that are not expected to be regularly added to

    Will seed themselves on creation with per-class specified seed data.
    """

    """ Data that should be seeded into the database when it is created """
    seeds = { 'columns': [], 'rows': [] }

    @classmethod
    def create_table(cls, seed=True, safe=True, **options):
        if cls.table_exists():
            seed = False

        super(BaseModel, cls).create_table(safe, **options)

        if seed:
            cls.seed()

    @classmethod
    def seed(cls):
        """
        Seeds the database with initial values
        """
        for row in cls.seeds['rows']:
            kwargs = { column: value for column, value in zip(cls.seeds['columns'], row) }
            cls(**kwargs).save()


class Tag(ClosedModel):
    """
    A TEI tag
    """

    """ The name of the tag """
    name = CharField(unique=True)

    """ Data that should be seeded into the database when it is created """
    seeds = {
        'columns': ['name'],
        'rows': [['persName'], ['placeName'], ['orgName']]
    }

    def __repr__(self):
        return self.name


class Entity(OpenModel):
    """
    A single entity; can have many lemmas
    """

    """ The ref attribute for the entity """
    name = CharField(unique=True)

    """ The kind of TEI tag the entity gets """
    tag = ForeignKeyField(Tag, backref='entities')

    def __init__(self, **kwargs):
        if 'tag' in kwargs and isinstance(kwargs['tag'], str):
            # Query the database and loads in the appropriate foreign key if the
            # provided tag name is a string
            kwargs['tag'] = Tag.get(Tag.name == kwargs['tag'])
        super(OpenModel, self).__init__(**kwargs)

    def __str__(self):
        return '#' + self.name


class Lemma(OpenModel):
    """
    An instance of a named entity. Any single NE may have multiple Lemma entries.
    """

    """ The name used for this instance """
    name = CharField()

    """ The entity that this lemma points to """
    entity = ForeignKeyField(Entity, backref='lemmas')

    def __init__(self, **kwargs):
        if 'entity' not in kwargs and 'tag' in kwargs:
            # If an entity wasn't explicitly provided, try to generate one based on the
            # lemma
            name = re.sub(' ', '_', kwargs['name'])
            try:
                entity = Entity.get(name=name)
            except:
                entity = Entity.create(name=name, tag=kwargs['tag'])
            kwargs['entity'] = entity

        super(OpenModel, self).__init__(**kwargs)

    def __str__(self):
        return self.name

    @property
    def aliases(self):
        """
        Retrieves all of the other lemmas used for this lemma's entity
        """
        return [alias for alias in self.entity.lemmas if not alias == self]

    def link_to(self, other):
        """
        Links this lemma to another entity

        If linking this lemma causes its previous entity to become stranded, the old
        entity will be deleted from the database.

        :param other: An Entity, a Lemma, or the name of an Entity or Lemma
        :type other: Union[Entity, Lemma str]
        """
        if isinstance(other, str):
            try:
                other = Entity.get(name=other)
            except:
                other = Lemma.get(name=other)

        if isinstance(other, Lemma):
            other = other.entity

        if isinstance(other, Entity):
            temp = self.entity

            self.entity = other 
            self.save()

            if temp.lemmas.count() == 0:
                temp.delete_instance()


def initialize():
    """
    Creates the database
    """
    DB.create_tables([Tag, Entity, Lemma])


# Open a database connection as soon as the module is loaded, and make sure it gets
# closed when the program terminates
DB.connect()
atexit.register(DB.close)

