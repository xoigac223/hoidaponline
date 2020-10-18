from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'sql12371461'
app.config['MYSQL_DATABASE_PASSWORD'] = 'fiDgrddexu'
app.config['MYSQL_DATABASE_DB'] = 'sql12371461'
app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net'

mysql.init_app(app)