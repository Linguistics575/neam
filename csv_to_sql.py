import sqlite3
import csv
connection = sqlite3.connect("test.db")
sql_command = "CREATE TABLE MyTable(placeholder VARCHAR(20));"
cursor = connection.cursor()
#cursor.execute(sql_command)

with open ('test.csv', 'r') as f:
    reader = csv.reader(f)
    columns = next(reader) 
    for i in columns:
    	print(i)
    query = 'insert into MyTable({0}) values ({1})'
    query = query.format(','.join(columns), ','.join('?' * len(columns)))
    for data in reader:
        cursor.execute(query, data)
    cursor.commit()

cursor.execute("SELECT * FROM alias") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)