# models.py

from flask import redirect, url_for
import sqlite3

def getDB():
    conn = sqlite3.connect("./data/database.db")
    return conn

def getAllBooks():
    conn = getDB()
    curs = conn.cursor()
    books = curs.execute("SELECT * FROM books").fetchall()
    conn.close()
    return books

def insert(name, author, count):
    conn = getDB()
    curs = conn.cursor()
    curs.execute(
        "INSERT INTO books(name, author, count) VALUES(?, ?, ?)", (name, author, count))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

def update(name, author, count, id):
    conn = getDB()
    curs = conn.cursor()
    curs.execute("UPDATE books SET name = ?, author = ?, count = ? WHERE id = ?", (name, author, count, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

def delete(id):
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    curs.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("index"))
