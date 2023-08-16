from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo


class UserLoginForm(FlaskForm):

    email = StringField("Email", [DataRequired()])
    password = StringField("Password", [DataRequired()])
    save = SubmitField('Login')
