from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField("Entry")


class RegisterForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=15)])
    password2 = PasswordField("Repeat password: ", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Entry")
