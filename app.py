from flask import render_template, redirect, url_for, flash
from sqlalchemy import orm

from database.db_operations import DbOperations
from database.model.user import User
from forms.accountform import AccountForm

from forms.bankform import BankForm
from forms.clientform import ClientForm
from forms.userloginform import UserLoginForm
from forms.userregistrationform import UserRegistrationForm

from init import app, db
from database.model.bank import Bank
from database.model.bankaccount import BankAccount
from database.model.person import Person
from flask_login import LoginManager, UserMixin, \
    current_user, \
    logout_user, login_user, login_required
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "prisijungti"


import os
SECRET_KEY = "opaopaopapaap123!000"
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/index')
@app.route('/homepage')
@app.route('/')
def index():
    return render_template('homepage.html')



@app.route("/banks/<message>")
@app.route("/banks")
@login_required
def banks(message=""):

    banks = Bank.query.all()

    return render_template('banks.html', banks=banks, message=message)


@app.route("/add-bank", methods=["GET", "POST"])
def add_bank():

    bank_form = BankForm()

    if bank_form.validate_on_submit():

        b = Bank(name=bank_form.name.data,address=bank_form.address.data,
                 bank_code=bank_form.bankcode.data, swift_code=bank_form.swiftcode.data)

        DbOperations.save(b)
        message = f"Bank {bank_form.name.data} has been successfully saved"
        return redirect(url_for('banks', message=message))
    else:
        return render_template("add_bank.html", bank=bank_form)


@app.route("/bank/delete/<int:id>")
def delete_bank(id):
    bank = DbOperations.get_bank(id)
    print(bank)
    if bank:
        db.session.delete(bank)
        db.session.commit()
        return redirect(url_for("banks"))
    else:
        return False


@app.route("/clients/<string:message>")
@app.route("/clients")
def clients(message=""):

    clients = DbOperations.get_all(Person)

    return render_template('clients.html', clients=clients, message=message)


@app.route("/client/add", methods=["GET", "POST"])
def add_client():

    clientform = ClientForm()
    message = f"New Client {clientform.firstname.data} " \
              f"{clientform.lastname.data} has been saved"
    if clientform.validate_on_submit():

        client = Person(*clientform)
        DbOperations.save(client)

        return redirect(url_for('clients', message=message))

    else:
        return render_template('add_client.html', client=clientform)


@app.route("/client/delete/<int:id>")
def delete_client(client_id):
    message = ""
    client = Person.query.get(client_id)
    if client:
        message = f"client {client.first_name} {client.last_name} has been deleted"
        db.session.delete(client)
        db.session.commit()
    return redirect(url_for("clients", message=message))


@app.route("/accounts")
def accounts():
    # Create an SQLAlchemy session
    # session = db.session()

    # Retrieve the BankAccount object with lazy-loaded bank attribute
    # account = session.query(BankAccount).get(1)

    # Access the bank attribute, which triggers lazy loading
    # bank_name = account.bank.name  # This should work now
    # print(f"bank_name {bank_name}")
    # Close the session to release resources
    # session.close()



    # with app.app_context():

    # accounts = BankAccount.query.all()

    # accounts = DbOperations.get_all(BankAccount)

    all_accounts = db.session.query(BankAccount)\
        .options(orm.joinedload(BankAccount.bank),
                 orm.joinedload(BankAccount.person)).all()
    return render_template('accounts.html', accounts=all_accounts)

@app.route("/delete_account/<int:id>")
def delete_account(id):

    account = BankAccount.query.get(id)
    if account:
        db.session.delete(account)
        db.session.commit()
    return redirect(url_for('accounts'))


@app.route("/account/add-new", methods=["GET", "POST"])
def add_account():

    account_form = AccountForm()
    if account_form.validate_on_submit():

        account = BankAccount(account_number=account_form.accountnumber.data)
        account.bank_id = account_form.bank.data.id
        account.person_id = account_form.client.data.id

        DbOperations.save(account)
        return redirect(url_for('accounts'))
    else:
        return render_template('add_account.html', bankaccount=account_form)




@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You have already logged in",'warning')
        return redirect(url_for('index'))

    user_form = UserRegistrationForm()

    if user_form.validate_on_submit():
        uemail = user_form.email.data
        upassword = bcrypt.generate_password_hash(user_form.password.data)\
            .decode('utf-8')
        user = User(email=uemail, password=upassword)

        db.session.add(user)
        db.session.commit()
        flash("User has been added", 'success')
        return redirect(url_for('index'))
    else:
        return render_template('register.html', form=user_form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login",methods=["GET","POST"])
def loginuser():
    if current_user.is_authenticated:
        flash("You have already logged in", 'warning')
        return redirect(url_for('index'))
    else:
        user = UserLoginForm()
        if user.validate_on_submit():
            usr = User.query.filter_by(email=user.email.data).first()
            if usr:
                pass_match = bcrypt.check_password_hash(usr.password, user.password.data)
                if pass_match:
                    login_user(usr)
                    flash("logged in successfully!!!", 'success')
                    return redirect(url_for('index'))
        else:
            return render_template('login.html', form=user)
if __name__ == "__main__":
    app.run(debug=True)

    # flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')


