
#If your form has multiple hidden fields, you can render them in one block using hidden_tag().

from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired,Length,Email,EqualTo
from wtforms import StringField,PasswordField,SubmitField,BooleanField


class MyForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])


class RegisterForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

