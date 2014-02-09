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

class Presentation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(200), unique=True)
	owner = db.Column(db.String(2000))
	votes = db.relationship('Vote', backref='vote_presentation')

	def __init__(self, url='', owner=''):
		self.url = url
		owner = owner

	def __repr__(self):
		return '<Presentation %r %r>' % (self.url, self.owner)

	def __unicode__(self):
		return self.url


class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	presentation = db.Column(db.Integer, db.ForeignKey('presentation.id'))
	user = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, user=None, presentation=None):
		self.user = user
		self.presentation = presentation

	def __repr__(self):
		return '<Vote %r %r>' % (self.presentation.url, self.user.email)

	def __unicode__(self):
		return self.user.email + ' ' + self.presentation.url
