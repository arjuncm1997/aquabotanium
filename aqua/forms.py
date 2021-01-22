from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from aqua.models import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SelectField


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address')
    phone = StringField('Contact No')
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),Length(min=8, max=8) ,EqualTo('password')])
    submit = SubmitField('Register')