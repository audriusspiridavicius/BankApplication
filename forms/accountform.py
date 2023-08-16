from flask_wtf import FlaskForm
from wtforms import *
from wtforms_sqlalchemy.fields import QuerySelectField
from database.db_operations import DbOperations
from database.model.bank import Bank

from init import app
from database.model.person import Person

def get_clients():
    with app.app_context():
        return Person.query.all()

def get_banks():
    with app.app_context():
        return Bank.query.all()
class AccountForm(FlaskForm):
    accountnumber = StringField('Account number')
    client = QuerySelectField(query_factory=get_clients, allow_blank=True)
    bank = QuerySelectField(query_factory=get_banks, allow_blank=True)

    save = SubmitField('Save')