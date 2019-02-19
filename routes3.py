
from flask import Blueprint, request, session, jsonify
from sqlalchemy.exc import IntegrityError
#from aks import db, requires_auth
from aks import app
from .models import User, Todo
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://prokask:q1234q123@localhost/aks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

mod_user = Blueprint('user', __name__, url_prefix='/api')
mod_todo = Blueprint('todo', __name__, url_prefix='/api')


@mod_user.route('/login', methods=['GET'])
def check_login():
	if 'user_id' in session:
		user = User.query.filter(User.id == session['user_id']).first()
		return jsonify(success=True, user=user.to_dict())

	return jsonify(success=False), 401


@mod_user.route('/login', methods=['POST'])
def login():
	try:
		email = request.form['email']
		password = request.form['password']
	except KeyError as e:
		return jsonify(success=False, message="%s not sent in the request" % e.args), 400
	
	user = User.query.filter(User.email == email).first()
	if user is None or not user.check_password(password):
		return jsonify(success=False, message="Invalid Credentials"), 400
		session['user_id'] = user.id
		return jsonify(success=True, user=user.to_dict())


@mod_user.route('/logout', methods=['POST'])
def logout():
	session.pop('user_id')
	return jsonify(success=True)


@mod_user.route('/register', methods=['POST'])
def create_user():
	try:
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
	except KeyError as e:
		return jsonify(success=False, message="%s not sent in the request" % e.args), 400

	if '@' not in email:
		return jsonify(success=False, message="Please enter a valid email"), 400
	u = User(name, email, password)
	db.session.add(u)
	try:
		db.session.commit()
	except IntegrityError as e:
		return jsonify(success=False, message="This email already exists"), 400
	return jsonify(success=True)


# todo route

@mod_todo.route('/todo', methods=['POST'])
@requires_auth
def create_todo():
	title = request.form['title']
	text = request.form['text']
	color = request.form['color']
	user_id = session['user_id']
	todo = Todo(title, text, color, user_id)
	db.session.add(todo)
	db.session.commit()
	return jsonify(success=True, todo=todo.to_dict())

@mod_todo.route('/todo', methods=['GET'])
@requires_auth
def get_all_todos():
	user_id = session['user_id']
	todos = Todo.query.filter(Todo.user_id == user_id).all()
	return jsonify(success=True, todos=[todo.to_dict() for todo in todos])

@mod_todo.route('/todo/<id>', methods=['GET'])
@requires_auth
def get_todo(id):
	user_id = session['user_id']
	todo = Todo.query.filter(Todo.id == id, Todo.user_id == user_id).first()
	if todo is None:
		return jsonify(success=False), 404
	else:
		return jsonify(success=True, todo=todo.to_dict())

@mod_todo.route('/todo/<id>', methods=['POST'])
@requires_auth
def edit_todo(id):
	user_id = session['user_id']
	todo = Todo.query.filter(Todo.id == id, Todo.user_id == user_id).first()
	if todo is None:
		return jsonify(success=False), 404
	else:
		todo.title = request.form['title']
		todo.text = request.form['text']
		todo.color = request.form['color']
		db.session.commit()
		return jsonify(success=True)

@mod_todo.route('/todo/<id>/done', methods=['POST'])
@requires_auth
def mark_done(id):
	user_id = session['user_id']
	todo = Todo.query.filter(Todo.id == id, Todo.user_id == user_id).first()
	if todo is None:
		return jsonify(success=False), 404
	else:
		todo.done = True
		db.session.commit()
		return jsonify(success=True)

@mod_todo.route('/todo/<id>/delete', methods=['POST'])
@requires_auth
def delete_todo(id):
	user_id = session['user_id']
	todo = Todo.query.filter(Todo.id == id, Todo.user_id == user_id).first()
	if todo is None:
		return jsonify(success=False), 404
	else:
			db.session.delete(todo)
			db.session.commit()
			return jsonify(success=True)

