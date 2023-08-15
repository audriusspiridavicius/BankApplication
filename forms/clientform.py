from flask_wtf import FlaskForm
from wtforms import *


class ClientForm(FlaskForm):

    firstname = StringField('First name')
    lastname = StringField('Last name')
    pin = StringField('Person identification number(PIN)')
    phone = StringField('Phone number')

    save = SubmitField('Save Client')

    def __iter__(self):
        return iter((self.firstname.data, self.lastname.data, self.pin.data, self.phone.data))
