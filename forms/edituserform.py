from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class EditUserForm(FlaskForm):
    
    email = StringField("Email",[DataRequired()])
    picture = FileField("Upload your picture",[FileAllowed(['jpg','png'])])
    save = SubmitField("Save")
     