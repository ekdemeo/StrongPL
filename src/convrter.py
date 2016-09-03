import sqlite3
import unicodedata

input = u'łękołody'
output = input.encode('utf-8', 'strict').decode('utf-8');

def uord(x): return '\\u' + str(ord(x));

for c in map(uord, output):
    print(c)



# conn = sqlite3.connect('StrongOrigin.twm')

# print("opened")

# cursor = conn.execute("SELECT data from content  limit 5")
# for row in cursor:
#    print(row[0])

# print("Operation done successfully");
# conn.close()


