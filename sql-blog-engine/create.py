import sqlite3


conn = sqlite3.connect('blog.db')
c = conn.cursor()

c.execute('''create table if not exists posts(title text, post text)''')
c.execute("INSERT INTO posts VALUES('test','testingtesttest')")

c.execute('''create table if not exists comments(post text)''')
c.execute("INSERT INTO comments VALUES('testingtesttest')")

c.execute('SELECT * FROM posts')
print c.fetchall()
c.execute('SELECT * FROM comments')
print c.fetchall()

conn.commit()
conn.close()
