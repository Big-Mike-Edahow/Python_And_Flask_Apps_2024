from flask import Flask, render_template, request, redirect, url_for, flash, session
import models as db
 
app = Flask(__name__)
app.secret_key = "A walk in the park is enjoyable."
 
@app.route('/')
def index():
    books = db.getAllBooks()
    return render_template("index.html", books=books)
 
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        count = request.form['count']
        db.insert(name, author, count)
        session.pop('_flashes', None)
        flash("Book Inserted Successfully")
        return redirect(url_for("index"))
 
@app.route("/update/<int:id>", methods = ['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        count = request.form['count']
        db.update(name, author, count, id)
        session.pop('_flashes', None)
        flash("Book Updated Successfully")
        return redirect(url_for("index"))

@app.route("/delete/<id>/")
def delete(id):
    db.delete(id)
    session.pop('_flashes', None)
    flash("Book Deleted Successfully")
    return redirect(url_for("index"))
 

if __name__ == "__main__":
    app.run(debug=True)

