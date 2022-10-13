import datetime
from logging import PlaceHolder
from tkinter.colorchooser import Chooser
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, EmailField 
from wtforms import SubmitField, DateTimeField, RadioField, IntegerField, TelField
from wtforms.validators import DataRequired, Email, Length


class FormInicio(FlaskForm):
    
    Email = StringField('User Name or Cell Phone', validators=[DataRequired(message='Se requiere que completes este campo'), 
        Length(min=3, message="debe se de min 8 caracteres")])  # 1 agos
    Password = PasswordField('Password', validators=[DataRequired(
        message='Se requiere que completes este campo'), Length(min=8, message="debe se de min 8 caracteres")])
    checkbox = BooleanField('Estoy de acuerdo', validators=[DataRequired(message='Se requiere que completes este campo')])
    enviar = SubmitField('Iniciar Sesión')

class FormUserNew(FlaskForm):
    Full_Name = StringField("Full Name", validators=[DataRequired(message='Se requiere que completes este campo')])
    Cell_Phone = TelField("Cell Phone", validators=[DataRequired(message='Se requiere que completes este campo'), 
        Length(min=10, message="debe se de min 8 caracteres")])
    ID = TelField('Id', validators=[DataRequired(message='Se requiere que completes este campo')])
    Email = EmailField('Email', validators=[DataRequired(message='Se requiere que completes este campo')])
    Password = PasswordField('Password', validators=[DataRequired(
        message='Se requiere que completes este campo')])
    Repeat_Password = PasswordField('password_confirmar', validators=[DataRequired(
        message='Se requiere que completes este campo')])
    Date = TelField('Date of Birth  D-M-Y') #DateTimeField
    radio = RadioField('Sexo:', choices=["Male", "Female"], validators=[DataRequired(message='Se requiere que completes este campo')])
    enviar = SubmitField('Check in')

class FormForgetPassword(FlaskForm):

    email = EmailField('Email', validators=[DataRequired(message='Se requiere que completes este campo')])
    
    Cell_Phone = TelField('Cell_phone', validators=[DataRequired(message='Se requiere que completes este campo'), 
        Length(min=10, message="debe se de min 10    caracteres")])

    New2_Password = PasswordField('password', validators=[DataRequired(
        message='Se requiere que completes este campo'), Length(min=10, message="debe se de min 8 caracteres"),
        ])
    Confirm2_Password = PasswordField('password_confirmar', validators=[DataRequired(
        message='Se requiere que completes este campo'), Length(min=10, message="debe se de min 8 caracteres"),
        ])
    enviar = SubmitField('Validated')
    Validated = SubmitField('Validated')



