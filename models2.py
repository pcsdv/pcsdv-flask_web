from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from aks import app
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://prokask:q1234q123@localhost/aks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(80),unique=True,nullable=False)
	email = db.Column(db.String(80),unique=True,nullable=False)
	image_file = db.Column(db.String(40),nullable=False,default='default.jpg')
	password = db.Column(db.String(80),nullable=False)
	posts = db.relationship('Post',backref='author',lazy=True)

	def __repr__(self):
		return '<User %r>' % self.username
#	def __init__(self,username,email,image_file,password):
#		self.username=username
#		self.email=email
#		self.image_file=image_file
#		self.password=password
#	return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100),nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
	content = db.Column(db.Text,nullable=False)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return '<User %r>' % self.title
#	def __repr__(self):
#		return f"Post('{self.title}','{self.date_posted}')"

