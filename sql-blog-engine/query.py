import sqlite3
conn = sqlite3.connect("p.db")

c = conn.cursor()

q = "select * from posts, text post"

result = c.execute(q)
print result
for r in result:
    print r
