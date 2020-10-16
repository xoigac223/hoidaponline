from flask import Flask, render_template
from flask_cors import CORS, cross_origin
 
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

CORS(app)	