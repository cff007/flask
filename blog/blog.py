#coding=utf-8
from pymongo import Connection
from flask import Flask,g,request,render_template,url_for,redirect,session,flash
from bson.objectid import ObjectId
from time import sleep

#configuration(配置blog的登录用户名密码)
USERNAME = 'admin'
PASSWORD = '123456'

app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
	con = Connection()
	g.db = con.blog

#设置密钥（要使用session，必须设置密钥）
#密钥可以在python命令行使用：
#import os 
#os.urandom(24)来获得密钥
app.secret_key = 'a\xcd\x94\xa2!\x8b\xd6\xa15\xef\xa8\xaeB!\xeb\xb6e\x83y[\xfe\xe3\x8f\xef'

#视图函数1：显示条目
@app.route('/')
def show_entires():
	entires = g.db.blog.find().sort('_id',-1)
	return render_template('show_entires.html',entires = entires)

#视图函数2：添加条目
@app.route('/add',methods=['POST'])
def add():
	if not session.get('logged_in'):   #判断是否登录(logged_in 键在会话中存在，若已登录即为 True )
		abort(401)
		flash('You should login first!')
	if not request.form['title']:
		flash('title should not be null')
	else:
		title = request.form['title']
		text = request.form['text']
		g.db.blog.insert({'title':title,'text':text})
		flash('New entry was successfully posed.')
	return redirect(url_for('show_entires'))

#视图函数3：删除
@app.route('/delete/<entry_id>')
def delete(entry_id):
	g.db.blog.remove({'_id':ObjectId(entry_id)})
	return redirect(url_for('show_entires'))

#视图函数4：登入和登出
@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != USERNAME:
			error = 'Invalid username'
		elif request.form['password'] != PASSWORD:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('Successfully login!')
			sleep(5)
			return redirect(url_for('show_entires'))
	return render_template('login.html',error = error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)   #使用字典的pop()方法，这个方法会从字典中删除这个键，如果这个键不存在则什么都不做
	flash('You were logged out')
	return redirect(url_for('show_entires'))

if __name__ == '__main__':
	app.run()