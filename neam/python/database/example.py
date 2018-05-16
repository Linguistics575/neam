from database import *
import database

# Create the database and populate it with tag names
database.initialize()

# Create a couple of entities
Lemma(name='Howard Carter', tag='persName').save()
Lemma(name='Howard', tag='persName').save()

print("Known entities:")
for entity in Entity.select():
    print(entity)
print()

# Link the entities together
howard = Lemma.get(name='Howard')
howard.link_to('Howard Carter')

print("Known entities:")
# The entity 'Howard' has now been deleted, since linking 'Howard' to 'Howard Carter' left it stranded
for entity in Entity.select():
    print(entity)
print()

print("Aliases of 'Howard Carter':")
for e in Lemma.get(Lemma.name == 'Howard Carter').aliases:
    print(e)
print()
print("Aliases of 'Howard':")
for e in Lemma.get(Lemma.name == 'Howard').aliases:
    print(e)
