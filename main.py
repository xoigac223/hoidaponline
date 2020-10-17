import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

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
if __name__ == "__main__":
	app.run()