from wtforms import Form, TextField, PasswordField, validators

class LoginForm(Form):
	email = TextField('Email Address', [validators.Required()])
	password = PasswordField('Password', [validators.Required()])
