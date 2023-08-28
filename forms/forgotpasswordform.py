from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ForgotPasswordForm(FlaskForm):
    email = StringField("Enter your email")
    
    send = SubmitField("Send")