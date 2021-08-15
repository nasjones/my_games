from flask import Flask, render_template, redirect, flash, jsonify, request, session, g, url_for
from models import User, Likes, Games, connect_db, db, reset_db, platform_setup, Platforms
from functools import wraps
from forms import LoginForm, SignUpForm, SearchForm
from sqlalchemy.exc import IntegrityError
from error_handling import integrityhandling
import os
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABSE_URL', 'postgresql:///my_games'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

USER_KEY = ""


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("Sorry you must be logged in to access that page", "danger")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def add_user_to_g():
    if USER_KEY in session:
        g.user = User.query.get(session[USER_KEY])
    else:
        g.user = None


def user_login(user):
    """Adds the user to the session"""
    session[USER_KEY] = user.id


def user_logout():
    if USER_KEY in session:
        del session[USER_KEY]


@app.route('/')
def home():
    if not g.user:
        return(render_template('anon-home.html'))
    form = SearchForm()
    form.platform.choices = [(
        plat.id, plat.name) for plat in Platforms.query.order_by('name').all()]
    return(render_template('home.html', likes=g.user.user_likes, form=form))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            user_login(user)
            flash(f"Hello, {user.username}!", "success")
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

        except IntegrityError as e:
            flash(integrityhandling(e), 'danger')
            return render_template('signup.html', form=form)

        user_login(user)
        flash(f"Hello, {user.username}!", "success")
        return redirect('/')

        flash("Username or Password incorrect.")

    return render_template('signup.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        user_logout()
        flash("successfully logged out", "success")
        return redirect('/')
    return render_template("logout.html")


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    print(f"{request.args.get('query')}")

    form = SearchForm()

    form.platform.choices = [(
        plat.id, plat.name) for plat in Platforms.query.order_by('name').all()]
    if form.validate_on_submit():
        print(form.platform.data, form.query.data)
    return(render_template('search.html', form=form))
