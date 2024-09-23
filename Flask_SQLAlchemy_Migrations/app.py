# app.py
# Flask SQLAlchemy Migrations

from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SECRET_KEY"] = "Time to get back to work"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)

    def __repr__(self):
        return f"<Product {self.name}>"

# Create Database with App Context
def create_db():
    with app.app_context():
        db.create_all()


@app.route("/")
def index():
    fruits = Product.query.all()
    return render_template("index.html", fruits=fruits)

@app.route("/about")
def about():
    return render_template("about.html")


# Run Main Program
if __name__ == "__main__":
    create_db()
    app.run(debug=True)

