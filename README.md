### flask快速入门
'''python
from flask import Flask
from flask import render_template	#模板渲染

app = Flask(__name__)

@app.route('/hello')		#decrator绑定URL
@app.route('/hello/<name>')
def hello(name = None):
	#return 'hello world'
	return render_template('hello.html', name = name)
	#模板渲染
'''
情况1: app为模块:
/application.py
/templates
    /hello.html

情况2: app为包:
/application
    /__init__.py
    /templates
        /hello.html
'''

@app.route('/user/<username>')
def show_user_profile(username):
	return 'User: %s' % username

#构造URL
from flask import url_for
with app.test_request_context():
	print(url_for('hello_world'))
	print(url_for('hello_world', next = '/'))
	print(url_for('show_user_profile', username = 'John Doe'))

#HTTP方法
#请求对象
from flask import request
@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		#do_the_login()
		if valid_login(request.form['username'],
						request.form['password']):
			return log_the_user_in(request.form['username'])
		else:
			error = 'Invalid username/password'
	#if methods = 'GET' of the credentials were invalid
	return render_template('login.html', error = error)
	#else:
		#show_the_login_form()

#静态文件
#md static
url_for('static', filename = 'style.css')
#储存在static/style.css

#文件上传
from flask import request
from werkzeug import secure_filename

@app.route('/upload', method = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['the_file']
		#f.save('/var/www/uploads/uploaded_file.txt')
		f.save('/var/www/uploads' + secure_filename(f.filename))

#读取cookies
from flask import request

@app.route('/')
def index():
	username = request.cookies.get('username')

#存储cookies
from flask import make_response

@app.route('/')
def index():
	resp = make_reaponse(render_template(...))
	resp.set_cookies('username', 'the username')
	return resp

#重定向和错误
from flask import abort, redirect, url_for

@app.route('/')
def index():
	return redirect(url_for('login'))	#重定向

@app.route('/login')
def login():
	abort(401)		#放弃请求并返回错误代码
	this_is_never_executed()

#定制错误页面
from flask import render_template
from flask import make_response

@app.errorhandler(404)
def page_not_found(error):
	#return render_template('page_not_found.html'), 404
	resp = make_response(render_template('error.html'), 404)
	resp.headers['X-Something'] = 'A value'
	return resp

#会话
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#消息闪现
flash()
get_flashed_messages()

#日志记录
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')

#整合WSGI中间件
from werkzeug.contrib.fixers import LighttpdCGIRootFix 	#整合WSGI中间件
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)

if __name__ == '__main__':
	#app.debug = True
	app.run(debug = True)	#app.run(host = '0.0.0.0') 监听所有公网IP
'''