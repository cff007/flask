#coding=utf-8
from flask import Flask,request,render_template

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return "hello world"

#模版渲染
#get方法，动态title,user_name
@app.route('/login_1')
def login_1():
	user_name = request.args.get('user','No user')         #在url后面加上参数?user=cff后刷新，页面输出 Welcome cff
														   #如果url没有?url参数，页面输出Welcome No user
	return render_template('login.html',title = 'form',user = user_name)




#post方法
@app.route('/login_2',methods=['GET','POST'])
def login_2():
	user_name = request.args.get('user','No user')
	if request.method == 'POST':
		return "this is a post"
	return render_template('login.html',title = 'Login',user = user_name)


#获得表单数据
@app.route('/login_3',methods=['GET','POST'])
def login_3():
	user_name = request.args.get('user','No user')
	if request.method == 'POST':
		print request.form.to_dict()
		return 'ok'
	return render_template('login.html',title = 'Login',user = user_name)


@app.route('/logout')
def logout():
	return "logout"

@app.route('/hello')
def hello():
	return 'this is route hello!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

@app.route('/users/<user_id>')
def show_post(user_id):
	return str(user_id)

@app.route('/bugs/<bug_id>')
def show_bugs(bug_id):
	return str(bug_id)

@app.route('/search')
def search():
	return request.args.get('kw','not found')
#访问http://localhost:5000/search?kw=adfagadfg，返回adfagadfg
#访问http://localhost:5000/search，这样没有kw关键字，返回not found

if __name__=='__main__':
	app.run()
