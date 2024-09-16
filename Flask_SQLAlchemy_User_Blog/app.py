# app.py
# Flask SQLAlchemy User Blog

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, LoginManager, UserMixin, logout_user, login_required
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '4d4c18d8d33c8c704705'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

def create_db():
    with app.app_context():
        db.create_all()

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable =False)
    last_name = db.Column(db.String(50), nullable =False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash =  db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'User<{self.username}>'

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

@login_manager.user_loader
def user_loader(id):
    return Users.query.get(int(id))

@app.route('/')
def index():
    posts = Posts.query.all()
    return render_template ("index.html", posts=posts)

@app.route('/view/<int:id>', methods = ['GET'])
def view_blog(id):
    post = Posts.query.get_or_404(id)
    return render_template('view.html', post=post)

@app.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':        
        title = request.form.get('title')
        author = current_user.username
        content = request.form.get('content')
        post = Posts(title=title, author=author, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    post = Posts.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('edit.html', post=post)
    elif request.method == 'POST' :
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for("index"))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Users.query.filter_by(username = username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST' :
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        user =  Users.query.filter_by(username= username).first()
        if user:
            return redirect(url_for('register'))
        email_exists = Users.query.filter_by(email=email).first()
        if email_exists:
            return redirect(url_for('register'))
        
        password_hash = generate_password_hash(password)
        new_user = Users(first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/delete/<int:id>', methods = ['GET'])
@login_required
def delete(id):
    post = Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    create_db()
    app.run(debug=True)

