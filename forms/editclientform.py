from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EditClientForm(FlaskForm):
    first_name = StringField("First Name",[DataRequired()])
    last_name = StringField("Last Name",[DataRequired()])
    pin = StringField("Person identification number",[DataRequired()])
    phone = StringField("Phone number")
    
    save = SubmitField("Save")