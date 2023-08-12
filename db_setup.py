from flask import Flask
from test import db, migrate
from database.model.bank import Bank
from database.model.bankaccount import BankAccount
from database.model.person import Person
# db = SQLAlchemy()
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_application.db'
# db.init_app(app)


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_application.db'
    db.init_app(app)
    migrate.init_app(app, db)
    return app