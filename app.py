from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS, cross_origin
import requests
 
app = Flask(__name__)

@app.route('/')
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
		list_users = requests.get("http://127.0.0.1:5000/user/{}/{}".format(username, password)).json()
		if len(list_users) == 1:
			requests.put("http://127.0.0.1:5000/update/{}".format(list_users[0]['id']))
			return redirect(url_for("index"))
	return render_template('login.html')
	

	
CORS(app)	