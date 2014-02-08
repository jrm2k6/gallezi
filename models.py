import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper, ColumnProperty

db = SQLAlchemy()

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	#votes = db.relationship('Vote', backref='vote_user', lazy='dynamic')

	def __init__(self, email=''):
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.email

	def __str__(self):
		return self.email

class Presentation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(200), unique=True)
	#votes = db.relationship('Vote', backref='vote_presentation', lazy='dynamic')

	def __init(self, url=''):
		self.url = url

	def __repr__(self):
		return '<User %r>' % self.url

	def __str__(self):
		return self.url


class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	presentation = db.Column(db.Integer, db.ForeignKey('presentation.id'))
	user = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init(self, user=None, presentation=None):
		self.user = user
		self.presentation = presentation

	def __repr__(self):
		return '<Vote %r>' % self.presentation.url + ' ' + self.user.email

	def __str__(self):
		return self.user.email + ' ' + self.presentation.url
