from db_setup import db


class BankAccount(db.Model):
    __tablename__ = 'bankaccount'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column('accountnumber', db.String(50), unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))

    bank = db.relationship('Bsnk', back_populates='accounts')
    person = db.relationship('Person', back_populates='accounts')