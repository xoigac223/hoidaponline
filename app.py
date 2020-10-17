from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from user import User, users, uname
from flask_login import LoginManager
import requests
from flask_socketio import SocketIO, send
from questions import Question, getQuestions


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)


@app.route('/', methods=["GET"])
def index():
	return render_template('index.html')
	

@app.route('/c')
def hoc_c():
	return render_template('c.html')

@app.route('/roadmap/frontend')
def roadmap_frontend():
	return render_template('frontend.html')

@app.route('/login', methods=["GET", "POST", "PUT"])
def login():
	if len(request.form) > 0:
		username = request.form['username']
		password = request.form['password']
		user = requests.get("http://127.0.0.1:5000/user/{}/{}".format(username, password)).json()
		if len(user) == 1:
			id = user[0]['id']
			uname = user[0]['username']
			pword = user[0]['password']
			status = user[0]['status']
			coin = user[0]['coin']
			u = User(id, uname, pword, status, coin)
			users[uname] = u
			requests.put("http://127.0.0.1:5000/update/{}".format(u.id))
			return redirect(url_for('nguoidung', uname = u.uname))
	return render_template('login.html')
	
@app.route('/<uname>',methods=["GET", "POST"])
def nguoidung(uname):
	user ={}
	user[uname] = users[uname].uname	
	user['status'] = users[uname].status
	user['coin'] = users[uname].coin
	return render_template('user.html', Template_uname = uname, user = user)

@app.route('/index/<uname>', methods=["GET", "POST"])
def index_user(uname):
	return render_template('index_user.html')

@app.route('/chatroom/<username>/')
def chatroom(username):
	return render_template('chatroom.html', template_username = username)

@app.route('/mentor')
def mentor():
	list_questions = getQuestions()
	return render_template('mentor.html', template_list_questions = list_questions, template_name = "mentor")

@app.route('/ask/<u_name>', methods=["GET", "POST"])
def ask(u_name):
	requests.get("http://127.0.0.1:5000/add_question")
	if len(request.form) > 0:
		title = request.form["title"]
		body = request.form["body"]
		coin = request.form["coin"]
		question = {
    		"title" : title,
    		"body" : body,
    		"user_ask" : u_name,
    		"coin" : coin
		}
		requests.post("http://127.0.0.1:5000/add_question", json = question) 
		return redirect(url_for('chatroom', username = u_name))
	return render_template('ask.html')

CORS(app)	