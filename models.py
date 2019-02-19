
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from aks.db import db


class User(db.Model):
	___tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))
	password = db.Column(db.String(80))
	admin = db.Column(db.Boolean)
	

	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.password, password)
	
	def to_dict(self):
		return {
			'id' : self.id,
			'name': self.name,
			'email': self.email,
			}

	def __repr__(self):
			#	return f"('{self.name },{self.email}')"
		return "User<%d> %s" % (self.id, self.name)


# todo class

class Todo(db.Model):
	__tablename__ = 'todo'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(255))
	text = db.Column(db.String(1000))
	color = db.Column(db.String(24))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	done = db.Column(db.Boolean, default=False)
	
	def __init__(self, title, text, color, user_id):
		self.title = title
		self.text = text
		self.color = color
		self.user_id = user_id
	
	def to_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'text': self.text,
			'color': self.color,
			'done': self.done,
			}
	
	def __repr__(self):
		return "Todo<%d> %s" % (self.id, self.title)

class Patient(db.Model):
	___tablename__ = 'patient'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(50))
	code = db.Column(db.String(10), unique=True)
	address = db.Column(db.String(100))
	age = db.Column(db.String(10)) 

	def __init__(self, name, code, address, age):
		self.name = [name]
		self.code = [code]
		self.address = [address]
		self.age = [age]

