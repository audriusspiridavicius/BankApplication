from db_setup import db


class Bank(db.Model):

    __tablename__ = 'bank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(300))
    bank_code = db.Column('bankcode', db.String(20))
    swift_code = db.Column('swiftcode', db.String(20))

    accounts = db.relationship('BankAccount', back_populates='bank')


