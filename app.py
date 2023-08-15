from flask import render_template, redirect, url_for
from sqlalchemy import orm

from database.db_operations import DbOperations

from forms.bankform import BankForm
from forms.clientform import ClientForm

from init import app, db
from database.model.bank import Bank
from database.model.bankaccount import BankAccount
from database.model.person import Person

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/homepage')
@app.route('/')
def index():
    return render_template('homepage.html')



@app.route("/banks/<message>")
@app.route("/banks")
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
def delete_client(id):
    message = ""
    client = Person.query.get(id)
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
        # accounts = DbOperations.get_all(BankAccount)
    accounts = db.session.query(BankAccount)\
        .options(orm.joinedload(BankAccount.bank),
                 orm.joinedload(BankAccount.person)).all()
    # print(accounts)
        # for account in accounts:
        #     print(account.bank.name)
        #     print(account.person.first_name)

        # print(accounts.bank.name)
    return render_template('accounts.html', accounts=accounts)

@app.route("/delete_account/<int:id>")
def delete_account(id):
    return redirect(url_for('accounts'))
if __name__ == "__main__":
    app.run(debug=True)



