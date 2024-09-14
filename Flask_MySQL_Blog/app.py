# app.py
# Flask MySQL Blog

from flask import Flask, render_template, request, redirect, url_for, flash, session
from utilities import getAllPosts, getPost
from db import getDB

app = Flask(__name__)
app.config["SECRET_KEY"] = "Got it to work this time."

@app.route('/')
def index():
    posts = getAllPosts()
    return render_template('index.html', posts=posts)

@app.route('/view/<int:post_id>',  methods=['GET', 'POST'])
def view(post_id):
    if request.method == "GET":
        post = getPost(post_id)
        conn = getDB()
        curs = conn.cursor()
        curs.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
        comments = curs.fetchall()
        return render_template('view.html', post=post, comments=comments)
    elif request.method == "POST":
        content=request.form['content']
        conn = getDB()
        curs = conn.cursor()
        curs.execute("INSERT INTO comments(comment, post_id) VALUES(%s, %s)", (content, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'GET':
        return render_template("create.html")
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = getDB()
        curs = conn.cursor()
        curs.execute('INSERT INTO posts (title, content) VALUES (%s, %s)',(title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
@app.route("/edit_post/<int:post_id>", methods=("GET", "POST"))
def edit_post(post_id):
    if request.method == "GET":
        post = getPost(post_id)
        return render_template("edit.html", post=post)
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = getDB()
        curs = conn.cursor()
        curs.execute("UPDATE posts SET title = %s, content = %s WHERE post_id = %s", (title, content, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    conn = getDB()
    curs = conn.cursor()
    curs.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
    comments = curs.fetchall()
    if comments:
        curs.execute("DELETE FROM comments WHERE post_id =%s", (post_id,))
        conn.commit()
    curs.execute("DELETE FROM posts WHERE post_id =%s", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    conn = getDB()
    curs = conn.cursor()
    curs.execute("DELETE FROM comments WHERE comment_id =%s", (comment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)

