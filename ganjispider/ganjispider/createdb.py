import sqlite3

conn = sqlite3.connect("zufang.sqlite")
cursor = conn.cursor()

cursor.execute('insert into zufang values (\'北京\', \'50000\')')
print(cursor.rowcount)
cursor.close()
conn.commit()
conn.close()