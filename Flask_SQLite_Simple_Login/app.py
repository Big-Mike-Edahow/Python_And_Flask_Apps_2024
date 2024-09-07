# app.py
# Flask SQLite Simple Login

from flask import Flask, render_template, request
import models as db

app = Flask(__name__)
app.config["SECRET_KEY"] = "Between a rock and hard place."

@app.route('/', methods = ["GET", "POST"])
def index():
	if request.method == "GET":
		return render_template("index.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		db.insertUser(username, password)
		users = db.selectUsers()
		return render_template("index.html", users=users)
   		

if __name__ == "__main__":
    app.run(debug=True)

