from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length
from models import Platforms


class SignUpForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class SearchForm(FlaskForm):
    """Search form."""
    query = StringField('Query', validators=[DataRequired()])
    platform = SelectField('Platform', coerce=int)
    # choices=[(
    #     plat.id, plat.name) for plat in Platforms.query.order_by('name').all()], coerce=int)
