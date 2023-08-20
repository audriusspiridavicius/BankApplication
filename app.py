import secrets
from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import delete, orm

from database.db_operations import DbOperations
from database.model.user import User
from forms.accountform import AccountForm

from forms.bankform import BankForm
from forms.clientform import ClientForm
from forms.userloginform import UserLoginForm
from forms.userregistrationform import UserRegistrationForm
from forms.edituserform import EditUserForm
from forms.editclientform import EditClientForm

from init import app, db
from database.model.bank import Bank
from database.model.bankaccount import BankAccount
from database.model.person import Person
from flask_login import LoginManager, \
    current_user, \
    logout_user, login_user, login_required
from flask_bcrypt import Bcrypt

from PIL import Image

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginuser"
# login_manager.login_message = ''
# login_manager.login_message_category = 'any category you like'
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

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page',10,type=int)
    banks = Bank.query.filter_by().paginate(page=page, per_page=per_page)

    return render_template('banks.html', banks=banks, message=message)


@app.route("/add-bank", methods=["GET", "POST"])
@login_required
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
@login_required
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

    page = request.args.get('page', 1, type=int)
    clients = Person.query.filter_by().order_by(Person.id).paginate(page=page,per_page=10)
    
    return render_template('clients.html', clients=clients,
                           message=message)


@app.route("/client/add", methods=["GET", "POST"])
@login_required
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

@app.route("/client/delete", methods=["POST"])
@app.route("/client/delete/<int:id>/")
@login_required
def delete_client(id=0):
    if request.method == "POST":
        client_ids = request.form.getlist('client')
       
        db.session.execute(delete(Person).where(Person.id.in_(client_ids)))
        db.session.commit()
    else:
        client = Person.query.get(id)
        if client:
            flash(f"client {client.first_name} {client.last_name} has been deleted",'success')
            db.session.delete(client)
            db.session.commit()
        else:
             flash("Such Client doesn exist",'error')
            
    return redirect(url_for("clients"))


@app.route("/accounts")
def accounts():
    page = request.args.get('page',1,type=int)
    per_page = request.args.get('per_page',10,type=int)

    all_accounts = db.session.query(BankAccount)\
        .options(orm.joinedload(BankAccount.bank),
                 orm.joinedload(BankAccount.person)).paginate(page=page,per_page=per_page)
    return render_template('accounts.html', accounts=all_accounts)

@app.route("/delete_account/<int:id>")
@login_required
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
    user = UserLoginForm()
    if user.validate_on_submit():
        usr = User.query.filter_by(email=user.email.data).first()
        if usr:
            pass_match = bcrypt.check_password_hash(usr.password, user.password.data)
            if pass_match:
                login_user(usr)
                flash("logged in successfully!!!", 'success')
                return redirect(url_for('index'))
        flash("Your email or password doesnt match. Please try again",'warning')
    return render_template('login.html', form=user)

def savepicture(picture):
    pictures_folder = "static/pictures"
    _,extension = os.path.splitext(picture.filename)
    rnd = secrets.token_hex(10)
    filename = rnd + extension
    full_picture_path = os.path.join(app.root_path,pictures_folder,filename)
    
    pic = Image.open(picture)
    pic.thumbnail((250,250))
    pic.save(full_picture_path)
    
    return filename
    

@app.route("/edituser", methods=["POST", "GET"])
def edituser():
    
    usereditform = EditUserForm()
    
    if usereditform.validate_on_submit():
        if usereditform.picture.data:
            if current_user.picture != 'default.png':
                old_picture_path = os.path.join(app.root_path,'static/pictures',current_user.picture)
                os.remove(old_picture_path)
            current_user.picture = savepicture(usereditform.picture.data)
        current_user.email = usereditform.email.data
        db.session.commit()
        flash("Your profile has been updated", 'success')
        return redirect(url_for('index'))
    usereditform.email.data = current_user.email
    picture = url_for('static',filename=f'pictures/{current_user.picture}')
    
    
    return render_template('edituser.html', form=usereditform, picture=picture)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit/client/<int:clientid>', methods=["GET","POST"])
@login_required
def editclient(clientid):
    
    edit_client_form = EditClientForm()
    client = Person.query.get(clientid)
    
    if client:
        if edit_client_form.validate_on_submit():
            client.first_name = edit_client_form.first_name.data
            client.last_name = edit_client_form.last_name.data
            client.pin = edit_client_form.pin.data
            client.phone = edit_client_form.phone.data
            db.session.commit()
            flash("Data was updated succesfully.",'success')
            return redirect(url_for('clients'))
        
        edit_client_form.first_name.data = client.first_name
        edit_client_form.last_name.data = client.last_name
        edit_client_form.pin.data = client.pin
        edit_client_form.phone.data = client.phone

        return render_template('editclient.html',form=edit_client_form, client=client)
    flash("No such Client!",'warning')        
    return redirect(url_for('clients'))



if __name__ == "__main__":
    app.run(debug=True)

    # flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')


