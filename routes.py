#import os
from flask import request, render_template,redirect, url_for, flash,jsonify

from flaskext.mysql import MySQL

#from flask_mysqldb import MySQL
from aks import app
from aks.posts import posts 
#import MySQLdb
from aks.forms import RegisterForm, LoginForm, MyForm
from aks.models import User,Todo,Patient 
import mysql.connector
# same like this below
#from aks.forms import * 
#from aks.models import * 


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dolphin'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route('/')
def hello():
	return '<h1>Welcome to my site </h1>'

@app.route('/table',methods=['GET','POST'])
def table():
	#con = mysql.connect(USER="root",password="",HOST="localhost",DATABASE="dolphin")
	con = mysql.connect()				
	m = con.cursor()
	q = "SELECT * FROM remedy"
	m.execute(q)
	rez = m.fetchall()
	for el in rez:
		print(el)
	con.close()
	return render_template('table.html',title='table',mydata=rez)



@app.route('/search',methods=['GET','POST'])
def search():
	conn = mysql.connect()
	cursor= conn.cursor()
	cursor.execute("SELECT * FROM patient")
	row = cursor.fetchall()
	conn.close()
	return render_template('search.html',title='Search',search=row)


@app.route('/search1/<username>',methods=['GET','POST'])
def search1(username):
	#query = request.args.get('dgfs')
	conn = mysql.connect()
	cursor= conn.cursor()
	sql = "SELECT * FROM patient" %username
	#sql = "SELECT * FROM patient WHERE fname LIKE '%s'=fname"
	cursor.execute(sql)
	results = cursor.fetchone()
	conn.close()
	return render_template('search1.html',title='Search1',pp =results)


@app.route("/medicine", methods=['GET', 'POST'])
def medicine():
	c = mysql.connect()
	cur = c.cursor()
	cur.execute('SELECT * FROM table3')
	result = cur.fetchall()
	c.close()
	return render_template('medicine.html',title='Medicine',result=result)


@app.route('/miasum')
def miasum():
	#db = MySQLdb.connect("localhost", "root", "","box")
	conn = mysql.connect()
	cursor= conn.cursor()
	cursor.execute("SELECT * FROM talika")
	fetchdata = cursor.fetchall()
	conn.close()
	return render_template('miasum.html',title='Miasum',mydata=fetchdata)


@app.route('/home')
def home():
	return render_template('home.html',posts=posts,title='Home')

@app.route('/about')
def about():
	return render_template('about.html',title='About')

@app.route('/forms',methods=['GET','POST'])
def forms():
	if request.method == "POST":
			#fetch form data
		details = request.form
		name = details['name']
		code = details['code']
		address = details['address']
		age = details['age']
		cur = mysql.connection.cursor()
#		cur = c.cursor()
		cur.execute("INSERT INTO patient(name,code,address,age) VALUES('%s', '%s', '%s', '%s')",(name,code,address,age))
		mysql.connection.commit()
		cur.close()
		return 'success'
	return render_template('forms.html',title='Forms')


@app.route('/searches', methods=['GET', 'POST'])
def searches():
	if request.method == "POST":
		db = MySQLdb.connect(user="root", passwd="", db="dolphin", host="localhost")
		c = db.cursor()
		c.executemany("select * from patient where name = '%s'", request.form['search'])
		for r in c.fetchall():
			print (r[0],r[1],r[2])
		return redirect(url_for('searches'))

	return render_template('searches.html',title='Searches')



@app.route('/register/', methods=['GET','POST'])
def register():
	form = RegisterForm()	
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!','success')
		return redirect(url_for('home'))	
	return render_template('register.html',title='Register',form=form)


@app.route('/login/', methods=['GET','POST'])
def login():
	form = LoginForm()	
	if form.validate_on_submit():
		return redirect(url_for('success'))	
	return render_template('login.html',title='Login',form=form)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
	form = MyForm()
	if form.validate_on_submit():
		return redirect(url_for('success'))
	else:
		return render_template('submit.html',title='Submit', form=form)

@app.route('/success')
def success():
	return '<h1>Welcome to my site.Your form is submited </h1>'


@app.route('/teacher')
def hello_teacher():
	return '<h1>Hey Teacher How you are?</h1>'

@app.route('/students/<student>')
def hello_students(student):
	return '<h1>Hello %s How are you ?</h1>' %student

@app.route('/user/<name>')
def hello_user(name):
	if name == 'teacher':
		return redirect(url_for('hello_teacher'))
	else:
		return redirect(url_for('hello_students'))

@app.route('/users', methods=['GET'])
def get_all_users():
	
	users = User.query.all()
	output = []

	for user in users:
		user_data={}
		user_data['public_id'] = user.public_id
		user_data['name'] = user.name
		user_data['password'] = user.password
		user_data['admin'] = user.admin
		output.append(user_data)

	return jsonify({'users' : output})





@app.route('/dbpatient', methods=['GET','POST'])
def dbpatient():
	sgh = Patient.query.all()
	return render_template('dbpatients.html',pdbss=sgh,title='Dbpatients')


@app.route('/dbpatient/<username>', methods=['GET','POST'])
def shpw_dbpatient(username):
	pdbs = Patient.query.filter_by(name=username).first_or_404()
#	pdbs = db.session.query(Patient).first()
	return render_template('dbpatient.html',pdbss=pdbs, title= 'Dbpatient')

