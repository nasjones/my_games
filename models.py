from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from platforms import platforms
import re

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


def reset_db():
    db.drop_all()
    db.create_all()
    platform_setup()


class Likes(db.Model):

    __tablename__ = 'likes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    game_id = db.Column(
        db.Text,
        db.ForeignKey('games.id', ondelete='cascade')
    )

    def __repr__(self):
        return f'user id:{self.user_id}, game id:{self.game_id}'

    @classmethod
    def add_like(cls, user_id, game_id):
        new_like = Likes(user_id=user_id, game_id=game_id)
        db.session.add(new_like)
        return new_like


class Games(db.Model):
    __tablename__ = 'games'

    id = db.Column(
        db.Text,
        nullable=False,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    image_url = db.Column(
        db.Text
    )

    deck = db.Column(
        db.Text
    )

    def __repr__(self):
        return f'{self.name}'

    @classmethod
    def add_game(cls, id, name, description, image_url, deck):
        # print(description)
        # description = re.search("<p>(.*?)</p>", description)
        # print(description)
        game = Games(id=id, name=name, description=description,
                     image_url=image_url, deck=deck)
        db.session.add(game)
        return game


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    user_likes = db.relationship(
        "Games",
        secondary="likes",
        primaryjoin=(Likes.user_id == id),
        secondaryjoin=(Likes.game_id == Games.id)
    )

    def __repr__(self):
        return f'{self.username}'

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Platforms(db.Model):
    """Table for platforms"""

    __tablename__ = "platforms"

    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    name = db.Column(
        db.Text,
        nullable=False
    )


def platform_setup():
    for item in platforms:
        new_plat = Platforms(id=item['id'], name=item['name'])
        db.session.add(new_plat)
    db.session.commit()
