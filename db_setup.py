from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_application.db'
# db.init_app(app)


def create_app():
    from database.model.bank import Bank
    from database.model.bankaccount import BankAccount
    from database.model.person import Person
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_application.db'
    db.init_app(app)
    migrate.init_app(app, db)
    return app

db = SQLAlchemy()
migrate = Migrate()
app = create_app()