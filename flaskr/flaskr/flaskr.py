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
app.config.from_envvar('FLASKR_SETTINGS', silent = True)
#从配置文件中加载配置

#Connects to the specific database
def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode = 'r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialized the database.')

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

#断开链接
@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

#显示条目
@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select title, text from entries order by id desc')
																#id降序
	entries = cur.fetchall()
	return render_template('show_entries.html', entries = entries)

#添加条目
@app.route('/add', methods = ['POST'])
def add_entry():
	if not session.get('logged_in'):	#用户未登入
		abort(401)		#放弃请求并返回错误代码
	db = get_db()
	db.execute('insert into entries (title, text) values (?, ?)',
				[request.form['title'], request.form['text']])
				#使用?标记构建sql语句
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

#login
@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error = error)

#logout
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
