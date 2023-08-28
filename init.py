import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail



db = SQLAlchemy()
migrate = Migrate()


def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    path_to_db_file = os.path.join(basedir, 'bank_application.db')
    print(path_to_db_file)
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path_to_db_file}'
    db.init_app(app)
    migrate.init_app(app, db)
    return app

app = create_app()

from database.model.bank import Bank
from database.model.bankaccount import BankAccount
from database.model.person import Person
from database.model.user import User




app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'caudrius.ctestacccccount99@gmail.com'
app.config['MAIL_PASSWORD'] = 'qunxxjjtlhnnqido'

mail = Mail(app)