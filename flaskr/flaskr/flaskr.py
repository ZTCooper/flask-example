import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#create application
app = Flask('flaskr')
app.config.from_object('flaskr')

#configuration
app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'flaskr.db'),
	DEBUG = True,
	SECRET_KEY = 'development key',
	USERNAME = 'admin',
	PASSWORD = 'default'
	))
app.config.from_envvar('FLASK_SETTINGS', silent = True)
#从配置文件中加载配置

#Connects to the specific database
def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

if __name__ == '__main__':
	app.run()
