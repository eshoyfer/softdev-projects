# Run this script before using the site for the first time. It ensures that all 
# necessary tables are at least in existence!
import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()

q1 = '''
create table if not exists posts(title text, post text, username text)
'''

q2 = '''
create table if not exists ACCOUNTS(username text, passhash text)
'''

c.execute(q1)
c.execute(q2)
conn.commit()
conn.close()