from sqlalchemy import text
from init import db


class BankAccount(db.Model):
    __tablename__ = 'bankaccount'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column('accountnumber', db.String(50), unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))
    balance = db.Column(db.Float, server_default=text("0.0"))
    bank = db.relationship('Bank', back_populates='accounts')
    person = db.relationship('Person', back_populates='accounts')
