#coding=utf-8

from flask import Flask,render_template, request, url_for,make_response,abort,redirect
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return 'hello world!'

#-------------------------变量规则--------------------------
@app.route('/user/<username>')
def username(username):
	return "User %s" %username

#-------------------------重定向------------------------------
@app.route('/help/')
def help():
	return 'help page!'
#访问一个结尾不带斜线的 URL 会被 Flask 重定向到带斜线的规范 URL 去

@app.route('/list')
def list():
	return 'The list page!'
#访问结尾带斜线的 URL 会产生一个 404 “Not Found” 错误。

#-------------------------构建url-----------------------------

with app.test_request_context():
	print url_for('index')
	print url_for('help')
	print url_for('list',next='/')
	print url_for('username',username='Halon')

#-------------------------静态文件----------------------------
#url_for('static',filename='blog.css')

#-------------------------模版渲染------------------------------
@app.route('/form')   
def form():
	return render_template('form.html')          #这个模版没有参数

@app.route('/muban/<name>')
def muban(name=None):
#	return render_template('jinj2.html',name = "")   #这种情况，向html传递的name参数为空，html打印出hello world!
#	return render_template('jinj2.html',name = "aaa")  #这种情况，向html传递的name=aaa，html打印出hello aaa!
	return render_template('jinj2.html',name=name)   #这种情况，向html传递的参数name等于url中输入的name参数，html打印出hello ‘name’


#---------------------------请求对象request-------------------------------
@app.route('/login',methods=['POST','GET'])
def login():
	error = None
	if request.method == 'POST':
		if (request.form['username']) and (request.form['password']):    #获取表单输入的username和password项
#			return log_the_user_in(request.form['username'])
			return 'Login success!'
		else:
			error = 'Invalid username/password'
			return error
	return render_template('login.html',title='login',user='cff')


#---------------------------通过request的args属性访问URL中提交的参数------------------------------
@app.route('/login_1')
def login_1():
	a = request.args.get('title','None')       #获取url中提交的title参数
	return render_template('login.html',title=a,user='cff')

#---------------------------Cookies----------------------------------------------------

@app.route('/cookie')
def cookie():
	resp = make_response(render_template('login.html',title='cookie',user='cff'))
	resp.set_cookie('username','oo111oppp')        #这两句话是存储cookies.cookies是设置在响应对象上。
	username = request.cookies.get('username')		#读取之前设置的username cookie
	print username
	return resp  #这个是与存储cookie一起的，在响应对象上设置。


#------------------------------重定向 redirect() 和 错误 abort()---------------------------

@app.route('/admin')
def admin():
	return redirect(url_for('error'))       #访问 http://localhost:5000/admin被重定向到http://localhost:5000/error

@app.route('/error')
def error():
	abort(401)					#401:禁止访问。

'''
#制定错误页面，用errorhandler()装饰器
@app.errorhandler(401)
def page_forbidden(error):
	return render_template('page_forbidden.html'),401
'''

#----------------------关于响应 make_response()---------------------------------------

@app.errorhandler(401)
def page_forbidden(error):
	resp = make_response(render_template('page_forbidden.html'),401)
	resp.headers['X-Something'] = 'A value'     #抓包发现response头部多出一条 X-Something:A value
	return resp


#----------------------会话-----------------------------------------------------------------



if __name__=='__main__':
	app.run()