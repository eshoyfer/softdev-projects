from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3, hashlib

app = Flask(__name__)

app.secret_key="SOMETHINGUNIQUEANDSECRET" # Don't use this key if you were actually going to deploy!


# Given title and post, will add the values into the table accordingly
def toTable(title, post, username):

    # Setting up SQLite stuff.
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    # Does it exist? If not, create it.
    # In either case, insert the values as requested.
    c.execute('''create table if not exists posts(title text, post text, username text)''')
    c.execute('''INSERT INTO posts VALUES("%s", "%s", "%s")''' % (title, post, username))

    # A note on functionality: 
    # Given an identical title, the entries will coexist. 
    # A request for a particular title page will yield all entries with the same title.

    print c.fetchall()
    conn.commit()
    conn.close()

# Given a title, will return an iterable of associated blog posts.
# [List of Strings] 
def postsWithTitle(title):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()  

    q = '''
    SELECT * FROM POSTS WHERE title == "%s"
    ''' % (title)

    # We've got:
    # title, post, username columns

    sql_posts_table = c.execute(q)

    posts_list = []

    for row in sql_posts_table:
    #    print len(row)
    #    for i in range(len(row)):
    #        posts_list[n][i] = row[i]

        this_post = []

        for i in range(len(row)):
            this_post.append(row[i])

        posts_list.append(this_post)

    #print posts_list
    conn.close()

    return posts_list

def postsByUser(username):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()  

    q = '''
    SELECT * FROM POSTS WHERE username == "%s"
    ''' % (username)

    # We've got:
    # title, post, username columns

    sql_posts_table = c.execute(q)

    posts_list = []

    for row in sql_posts_table:
    #    print len(row)
    #    for i in range(len(row)):
    #        posts_list[n][i] = row[i]

        this_post = []

        for i in range(len(row)):
            this_post.append(row[i])

        posts_list.append(this_post)

    #print posts_list
    conn.close()

    return posts_list

# Is the username taken? Simple validation. We're allowed a wide range of usernames, really.
def validUsername(username):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()  

    q = '''
    SELECT USERNAME FROM ACCOUNTS WHERE USERNAME == "%s"
    ''' % (username)

    sql_users_table = c.execute(q) 
    users_list = []

    for user in sql_users_table:
        print user
        users_list.append(user[0])

    #print users_list
    conn.close()

    print username, users_list

    return username not in users_list

def validLoginUsername(username):
    return not validUsername(username)

# Given username, password attempt 
# Returns boolean if valid login 
def validLogin(username, password):

    if not validLoginUsername(username):
        return False

    m = hashlib.sha1()
    m.update(password)
    password_hash = m.hexdigest()
    q = '''
    SELECT passhash FROM ACCOUNTS WHERE username == "%s"
    ''' % (username)

    conn = sqlite3.connect('blog.db')
    c = conn.cursor()  

    sql_passhash_table = c.execute(q)
    

    passhash_list = []

    for passhash in sql_passhash_table:
        print passhash
        passhash_list.append(passhash[0])


    conn.close()

    if len(passhash_list) < 1:
        return False
    else:
        return password_hash == passhash_list[0]

@app.route("/home", methods = ["GET","POST"])
@app.route("/", methods = ["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        # Button press determination
        button = request.form['submit']
        print button

        # Search case:
        if button == "search":
            print request.form, "HERE"
            print request.form['title_search']
            print request.form['user_search']
            if (request.form["title_search"] != ""):
                if (request.form["user_search"] != ""):
                    flash("You can't perform two types of searches at once!")
                    return redirect(url_for('home')) 
                else:
                    query = request.form["title_search"]
                    print query
                    return redirect(url_for('title', title=query))
            else:
                if (request.form["user_search"] == ""):
                    flash("You didn't enter anything in either search field!")
                    return redirect(url_for('home'))
                else:
                    query = request.form["user_search"]
                    print query
                    return redirect(url_for('user', username=query))

        # Extract form data
        else:
            title = request.form["title"]
            post = request.form["post"]
            username = request.form["username"]
            password = request.form["password"]
            print title, post, username, password
            #button = request.form["b"]

            # Validate

            # Invalid case
            if not validLogin(username, password):
                flash("Invalid login! Did you make sure to register?")
                return redirect(url_for('home'))

            # Valid case

            # Add this new content to the table, and associate it with the username.

            toTable(title, post, username)
            flash("Post successfully added!")
            return render_template("home.html")


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        print "MADE IT"
        username = request.form["username"]
        password = request.form["password"]

        if not validUsername(username):
            flash("Username already taken!")
            return redirect(url_for('register'))

        # The following code runs in the event of a proper username selection

        m = hashlib.sha1()
        m.update(password)
        password_hash = m.hexdigest()

        conn = sqlite3.connect('blog.db')
        c = conn.cursor()

        c.execute('''create table if not exists accounts(username text, passhash text)''')
        print password_hash
        q = '''INSERT INTO ACCOUNTS VALUES("%s", "%s")''' % (username, password_hash)
        print q

        # Store the hash in the account info table
        c.execute(q)

        # Test 

        qt = ''' SELECT * FROM ACCOUNTS '''

        conn.commit()
        conn.close()

        flash("Successfully registered!")
        return redirect(url_for('home'))

@app.route("/<title>")
def title(title):

    posts = postsWithTitle(title)
    return render_template("title.html", posts=posts, title=title)

@app.route("/user/<username>")
def user(username):

    posts = postsByUser(username)
    return render_template("user.html", posts=posts, username=username)

@app.errorhandler(404)
def not_found(e): # Return rendering, 404
    return render_template('404.html'), 404

if __name__=="__main__":
    app.debug=True
    app.run()
    #app.run(host="0.0.0.0",port=8888)
