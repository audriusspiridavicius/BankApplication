from init import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column('firstname', db.String(100))
    last_name = db.Column('lastname', db.String(100))
    pin = db.Column('pin', db.String(50), unique=True)
    phone = db.Column(db.String(20))

    accounts = db.relationship('BankAccount', back_populates='person')

    def __init__(self, firstname, lastname, pin, phone):
        self.first_name = firstname
        self.last_name = lastname
        self.pin = pin
        self.phone = phone
