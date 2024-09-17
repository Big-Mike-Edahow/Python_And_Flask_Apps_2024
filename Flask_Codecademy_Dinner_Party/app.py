# app.py
# Codecademy Accounts Dinner Party

from flask import Flask, flash, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)
app.config["SECRET_KEY"] = "Slow and steady wins the race"

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# DinnerParty Model
class DinnerParty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(140))
    venue = db.Column(db.String(140))
    main_dish = db.Column(db.String(140))
    number_seats = db.Column(db.Integer)
    party_host_id = db.Column(db.Integer)
    attendees = db.Column(db.String(256))


# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


# Login Form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


# Dinner Party Form
class DinnerPartyForm(FlaskForm):
    date = StringField("Date", validators=[DataRequired()])
    venue = StringField("Venue", validators=[DataRequired()])
    main_dish = StringField("Dish", validators=[DataRequired()])
    number_seats = StringField("Number of Seats")
    submit = SubmitField("Create")


# RSVP Form
class RsvpForm(FlaskForm):
    party_id = StringField("Party ID", validators=[DataRequired()])
    submit = SubmitField("RSVP")


# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Index Route
@app.route("/")
def index():
    current_users = User.query.all()
    return render_template("index.html", current_users=current_users)

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(csrf_enabled=False)
    if request.method == "GET":
        return render_template("register.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("register.html", title="Register", form=form)

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(csrf_enabled=False)
    if request.method == "GET":
        return render_template("login.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("index"))
            else:
                return redirect(url_for("login"))
        return render_template("login.html", form=form)

# User Route
@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    dinner_parties = DinnerParty.query.filter_by(party_host_id=user.id)
    if dinner_parties is None:
        dinner_parties = []
    form = DinnerPartyForm(csrf_enabled=False)
    if request.method == "GET":
        return render_template("user.html", user=user, dinner_parties=dinner_parties, form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            new_dinner_party = DinnerParty(
                date=form.date.data,
                venue=form.venue.data,
                main_dish=form.main_dish.data,
                number_seats=int(form.number_seats.data),
                party_host_id=user.id,
                attendees=username,
            )
            db.session.add(new_dinner_party)
            db.session.commit()
            return redirect(url_for('profile', username=username))

# RSVP Route
@app.route("/rsvp/<username>", methods=["GET", "POST"])
@login_required
def rsvp(username):
    user = User.query.filter_by(username=username).first_or_404()
    dinner_parties = DinnerParty.query.all()
    if dinner_parties is None:
        dinner_parties = []
    form = RsvpForm(csrf_enabled=False)
    if request.method == "GET":
        return render_template("rsvp.html", user=user, dinner_parties=dinner_parties, form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            dinner_party = DinnerParty.query.filter_by(id=int(form.party_id.data)).first()
            # Try block
            try:
                dinner_party.attendees += f", {username}"
                db.session.commit()
                # Query to find the host of dinner_party
                host = User.query.filter_by(id=int(dinner_party.party_host_id)).first()
                # Add RSVP success message here:
                flash(
                    f"You RSVP'd to {host.username}'s dinner party on {dinner_party.date}!")
            # Except block
            except:
                # Add the RSVP failure message here
                flash("Please enter a valid Party ID to RSVP!")
            return redirect(url_for('rsvp', username=username))

# Logout Route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# About Route
@app.route("/about")
def about():
    return render_template("about.html")


def create_db():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_db()
    app.run(debug=True)

