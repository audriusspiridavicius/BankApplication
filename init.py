from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
migrate = Migrate()


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_application.db'
    db.init_app(app)
    migrate.init_app(app, db)
    return app

app = create_app()

from database.model.bank import Bank
from database.model.bankaccount import BankAccount
from database.model.person import Person
from database.model.user import User