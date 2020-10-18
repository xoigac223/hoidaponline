import pymysql
from app import app, socketio
from db_config import mysql
from flask import jsonify
from flask import flash, request
from questions import Question, getQuestions, question

@app.route('/user/<username>/<password>')
def user(username, password):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE username='{}' and password='{}'".format(username, password))
		row = cursor.fetchall()
		res = jsonify(row)
		res.status_code = 200
		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users")
		rows = cursor.fetchall()
		res = jsonify(rows)
		res.status_code = 200
 
		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
	try:
		sql = "UPDATE users SET status = 1 WHERE id={}".format(id)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql)
		conn.commit()
		res = jsonify('User updated successfully.')
		res.status_code = 200
		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update_question/<user_ask>/<coin>', methods=['PUT'])
def update_ques(user_ask, coin):
	try:
		icoin = int(coin)
		list_questions = getQuestions()
		q = question(list_questions, user_ask)
		cur_coin = q.coin - icoin
		sql = "UPDATE users SET coin = {} WHERE user_ask={}".format(cur_coin, user_ask)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql)
		conn.commit()
		res = jsonify('User updated successfully.')
		res.status_code = 200
		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/questions')
def questions():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM questions_online")
		rows = cursor.fetchall()
		res = jsonify(rows)
		res.status_code = 200
		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/add_question', methods=['POST'])
def add_question():
	try:
		_json = request.json
		_title = _json['title']
		_body = _json['body']
		_user_ask = _json['user_ask']
		_coin = _json['coin']

		sqlQuery = "INSERT INTO questions_online(title, body, user_ask, coin) VALUES(%s, %s, %s, %s)"
		data = (_title, _body, _user_ask, _coin,)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sqlQuery, data)
		conn.commit()
		res = jsonify('Student created successfully.')
		res.status_code = 200
		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
# if __name__ == "__main__":
# 	app.run()
if __name__ == '__main__':
    socketio.run(app)