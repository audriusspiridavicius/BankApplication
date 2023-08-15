from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class BankForm(FlaskForm):

    name = StringField('Bank name', [DataRequired()])
    address = StringField('Bank address', [DataRequired()])
    bankcode = StringField('Bank code', [DataRequired()])
    swiftcode = StringField('Swift code', [DataRequired()])
    save = SubmitField('Save')