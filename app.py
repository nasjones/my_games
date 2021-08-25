from flask import Flask, render_template, redirect, flash, jsonify, request, session, g, url_for
from models import User, Likes, Games, connect_db, db, platform_setup, Platforms
from functools import wraps
from forms import LoginForm, SignUpForm, SearchForm
from sqlalchemy.exc import IntegrityError
from error_handling import integrityhandling
from api_calls import search_api, single_game, similar_games
import math
import os


def page_not_found(e):
    """Handler for any 404 errors"""
    return render_template('404.html'), 404


app = Flask(__name__)
app.register_error_handler(404, page_not_found)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///my_games').replace("postgres://", "postgresql://", 1))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)


USER_KEY = ""


def login_required(f):
    """This is a wrapper that ensures any pages that require user access will redirect the user if they are not logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("Sorry you must be logged in to access that page", "danger")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def add_user_to_g():
    """This function adds the user object globally"""
    if USER_KEY in session:
        g.user = User.query.get(session[USER_KEY])
    else:
        g.user = None


def user_login(user):
    """Adds the user to the session"""
    session[USER_KEY] = user.id


def user_logout():
    """Removes the user from the session"""
    if USER_KEY in session:
        del session[USER_KEY]


@app.route('/')
def home():
    """Base route of the website with two different routes depending on whether a user is logged in or not"""
    # If user object hasn't been stored via the login process
    # then show them a different homepage
    if not g.user:
        return(render_template('anon-home.html'))
    return(render_template('home.html', likes=g.user.user_likes))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    # If user is already logged in redirect them to the homepage
    if g.user:
        return redirect('/')
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
    """Allows users to create an account"""
    # If user is already logged in redirect them to the homepage
    if g.user:
        return redirect('/')

    form = SignUpForm()
    if form.validate_on_submit():
        try:
            user = User.signup(form.username.data,
                               form.email.data,
                               form.password.data)
            db.session.commit()
        # Catches an error thrown when using duplicate information such
        # as an email already in use or a username thats been taken
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
    """Route allowing user to logout"""
    if request.method == 'POST':
        user_logout()
        flash("successfully logged out", "success")
        return redirect('/')
    return render_template("logout.html")


@app.route('/search/<title>/<int:platform>/<int:page>', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search(title=None, platform=None, page=1):
    """Route allowing user to utilize the power of the api and search for games by title"""
    # Sets the defaults for the page
    game_list = None
    pages = {}
    platforms = Platforms.query.order_by('name').all()
    game_data = search_api(title, platform, page)
    likes = [game.id for game in g.user.user_likes]

    # Checks if a search was carried out based on the input
    if game_data:
        game_list = game_data["results"]
        pages["amount"] = math.ceil(
            game_data["number_of_total_results"]/10)
        pages["query"] = title
        pages["platform"] = platform

    return(render_template('search.html', game_list=game_list, pages=pages, platforms=platforms, page=page, title=title, platform_id=platform, likes=likes))


@app.route('/game/<id>')
@login_required
def game_display(id):
    """Displays the information on a specific game"""
    # checks if the game is already in the database
    game = Games.query.filter_by(id=id).first()
    # if the game isnt in the database make an api call
    if not game:
        game_data = single_game(id)["results"]

        game = Games.add_game(
            id=game_data["guid"], name=game_data["name"], description=game_data["description"], image_url=game_data["image"]["medium_url"], deck=game_data["deck"])
    db.session.commit()
    # make the call to find similar games
    similar = similar_games(game.name)
    liked = (game in g.user.user_likes)
    return render_template('game.html', game=game, similar=similar, liked=liked)


@app.route('/api/like', methods=["POST"])
@login_required
def like_game():
    """Endpoint for users to update like on a game"""
    info = request.json["game"]
    # Check if the game is already in our database
    game = Games.query.get(info["id"])
    # If not add the game to our database
    if not game:
        game = Games.add_game(**info)

    new_like = Likes.add_like(user_id=g.user.id, game_id=game.id)
    db.session.commit()
    return jsonify({"new_like": new_like.id})


@app.route('/api/unlike', methods=["POST"])
@login_required
def unlike_game():
    """Endpoint allowing users to remove game from their likes"""
    # gets like id from the database
    like = Likes.query.filter_by(
        user_id=g.user.id, game_id=request.json["id"]).first()

    db.session.delete(like)
    db.session.commit()
    return jsonify({"deleted": like.id})
