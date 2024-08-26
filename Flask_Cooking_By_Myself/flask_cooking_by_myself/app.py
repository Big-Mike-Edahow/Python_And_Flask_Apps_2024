# app.py
# Flask SQLite Cooking by Myself

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "All is quiet along the Wasatch Front."

@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == 'POST':
    recipe = request.form["recipe"]
    meal = request.form["meal"]
    description = request.form["description"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]

    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute("INSERT INTO recipes(recipe, meal, description, ingredients, instructions) VALUES(?, ?, ?, ?, ?)",(recipe, meal, description, ingredients, instructions),)
    conn.commit()
    conn.close()

    return redirect(url_for('index'))
  elif request.method == 'GET':
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    recipes = curs.execute("SELECT * FROM recipes").fetchall()

    return render_template("index.html", recipes=recipes)

@app.route("/recipe", methods=["GET", "POST"])
def recipe():
  if request.method == 'POST':
    recipe_id = request.form["recipe_id"]
    author = request.form["author"]
    content = request.form["content"]

    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute("INSERT INTO comments(recipe_id, author, content) VALUES(?, ?, ?)", (recipe_id, author, content))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))
  elif request.method == 'GET':
    id = request.args.get("id")
    recipe_id = id

    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    recipe = curs.execute("SELECT * FROM recipes WHERE id=?", id).fetchone()
    comments = curs.execute("SELECT * FROM comments WHERE recipe_id=?", recipe_id).fetchall()
    instructions = curs.execute("SELECT instructions FROM recipes where id =?", id).fetchone()
    instructions = str(instructions[0])
    instructions = instructions.split('.')

    return render_template("recipe.html", recipe=recipe, instructions=instructions, comments=comments)
  
@app.route('/delete_recipe')
def delete_recipe():
    id = request.args.get("id")
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute('DELETE FROM recipes WHERE id = ?', id,)
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete_comment')
def delete_comment():
    id = request.args.get("id")
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute('DELETE FROM comments WHERE id = ?', id,)
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route("/about/")
def about():
  return render_template("about.html")
  
if __name__ == '__main__':
  app.run(debug=True)

