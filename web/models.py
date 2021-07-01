from app import db
from datetime import datetime
import re

class Message(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	fromUser = db.Column(db.String(128))
	text = db.Column(db.String(1024))

	def __repr__(self):
		return '{}: {}'.format(self.fromUser, self.text)
		

'''class user(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	login = db.Column(db.String(60))
	password = db.Column(db.String(120))
	customStyle = db.Column(db.Boolean(1))

	def __init__(self, *args, **kwargs):
		super (user, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '{} {}'.format(self.login, self.password)

class group_(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(40))
	users = db.Column(db.Text(60000))
	slug = db.Column(db.String(90), unique = True)

	def __init__(self, *args, **kwargs):
		super(group_, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '{}'.format(self.name)'''
