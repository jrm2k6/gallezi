import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper, ColumnProperty

db = SQLAlchemy()

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	votes = db.relationship('Vote', backref='vote_user')

	def __init__(self, email=''):
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.email

	def __unicode__(self):
		return self.email

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

class Presentation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(200), unique=True)
	owner = db.Column(db.String(2000))
	votes = db.relationship('Vote', backref='vote_presentation')

	def __init__(self, url='', owner=''):
		self.url = url
		self.owner = owner

	def __repr__(self):
		return '<Presentation %r %r>' % (self.url, self.owner)

	def __unicode__(self):
		return self.url


class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	presentation = db.Column(db.Integer, db.ForeignKey('presentation.id'))
	user = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, presentation=None, user=None):
		self.presentation = presentation
		self.user = user

	def __repr__(self):
		return '<Vote %r %r>' % (self.vote_presentation.url, self.vote_user.email)

	def __unicode__(self):
		return self.vote_user.email + ' ' + self.vote_presentation.url
