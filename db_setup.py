from flask import Flask, Response, render_template, request, redirect
from flaskext.mysql import MySQL


mysql = MySQL()
app = Flask(__name__)

def setup_db():
    config_db()
    return mysql

def create_connection():
    config_db()
    connection = mysql.connect()
    connection.autocommit(True)
    return connection

def config_db():
    app.config['MYSQL_DATABASE_USER'] = 'bb7d283420909b'
    app.config['MYSQL_DATABASE_PASSWORD'] = '4897db48'
    app.config['MYSQL_DATABASE_DB'] = 'heroku_3ed428654b91ed0'
    app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-05.cleardb.net'
    mysql.init_app(app)



