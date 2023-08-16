from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo


class UserRegistrationForm(FlaskForm):

    email = StringField("Email", [DataRequired()])
    password = StringField("Password", [DataRequired()])
    confirm_password = StringField("Confirm password", [
        DataRequired(),
        EqualTo('password', "passwords have to match")])

    save = SubmitField('Save')

    def __str__(self):
        return self.email
