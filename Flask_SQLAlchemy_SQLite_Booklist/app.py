# app.py
# MySQL Flask App

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
 
# Creating Flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = "One last weekend of fun."
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Creating SQLAlchemy instance
db = SQLAlchemy()

# Initializing Flask app with SQLAlchemy
db.init_app(app)

# Creating Models
class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, unique=True)
    author = db.Column(db.String(500), nullable=False)
    created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())


def create_db():
    with app.app_context():
        db.create_all()

# Home route
@app.route("/")
def index():
    books = Books.query.all()
    return render_template("index.html", books=books)
 
 
# Add data route
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template("books.html")
    elif request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        book = Books(
            title=title,
            author=author
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    

if __name__ == "__main__":
    create_db()
    app.run(debug=True)
