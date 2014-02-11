from wtforms import Form, TextField, PasswordField, validators

class LoginForm(Form):
	email = TextField('Email Address', [validators.Required()])
	password = PasswordField('Password', [validators.Required()])

class AddPresentationForm(Form):
	url = TextField('URL', [validators.Required(), validators.URL(require_tld=True, 
		message=u'Invalid url')])
	owner = TextField('Owner', [validators.Required()])
	password = PasswordField('Password for submission', [validators.Required()])
