import sqlite3
import csv
import sys
from database import *
import database

import_csv = open(sys.argv[1], 'r')
result = {}
with import_csv as f:
    reader = csv.reader(import_csv)
    for row in reader:
        result.setdefault(row[0],[])
        result[row[0]].append([])
        for value in row[1:]:
            result[row[0]][-1].append(value)
print(result)

for reference, list_of_entries  in result.items():
    for entry in list_of_entries:
        Lemma(name=entry[0], tag=entry[1]).save()
        ent = Lemma.get(name=entry[0])
        ent.link_to(reference)
