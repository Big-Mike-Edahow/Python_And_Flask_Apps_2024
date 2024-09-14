# utilities.py

from db import getDB

def getAllPosts():
    conn = getDB()
    curs = conn.cursor()
    curs.execute("SELECT * FROM posts")
    posts = curs.fetchall()
    return posts

def getPost(post_id):
    conn = getDB()
    curs = conn.cursor()
    query = 'SELECT * FROM posts WHERE post_id = %s'
    curs.execute(query, (post_id, ))
    post = curs.fetchone()
    return post

