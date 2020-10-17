from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from user import User, users, uname
from flask_login import LoginManager
import requests
from flask_socketio import SocketIO, send

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
	render_template('index_user.html')

@app.route('/chatroom')
def chatroom():
	return render_template('chatroom.html')

CORS(app)	