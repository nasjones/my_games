from flask import Flask, render_template, redirect, flash, jsonify, request, session, g, url_for
from models import User, Likes, Games, connect_db, db
from forms import LoginForm, SignUpForm
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABSE_URL', 'postgres///my_game'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

USER_KEY = ""


@app.before_request
def add_user_to_g():
    if USER_KEY in session:
        g.user = User.query.get(session[USER_KEY])
    else:
        g.user = None

    if not g.user and request.endpoint not in ['login', 'signup', 'home']:
        flash("You must be logged in to view this page so either login or signup.")
        return redirect(url_for('login'))


def user_login(user):
    """Adds the user to the session"""
    session[USER_KEY] = user.id


def user_logout():
    if USER_KEY in session:
        del session[USER_KEY]


@app.route('/')
def home():
    return(render_template('home.html'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            user_login(user)
            flash(f"Hello, {user.username}!")
            return redirect('/')

        flash("Username or Password incorrect.")

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(form.username.data,
                               form.email.data,
                               form.password.data)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        user_login(user)
        flash(f"Hello, {user.username}!")
        return redirect('/')

        flash("Username or Password incorrect.")

    return render_template('signup.html', form=form)
