import sqlite3

conn = sqlite3.connect('StrongOrigin.twm')

print("opened")

cursor = conn.execute("SELECT data from content  limit 5")
for row in cursor:
   print(row[0])

print("Operation done successfully");
conn.close()


