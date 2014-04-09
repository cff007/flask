#coding=utf-8
import os
from pymongo import Connection
from flask import Flask,g,render_template,request,flash,url_for,redirect,session,send_from_directory
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

upload_path = 'uploads'

app = Flask(__name__)
app.debug = True


@app.before_request
def before_request():
	conn = Connection()
	g.db = conn.bugbank

app.secret_key = 'a\xcd\x94\xa2!\x8b\xd6\xa15\xef\xa8\xaeB!\xeb\xb6e\x83y[\xfe\xe3\x8f\xef'

@app.route('/')
def index():
	bugs = g.db.bugs.find().sort('_id',-1)
	print g.db.bugs.find_one()
	return render_template('index.html',bugs = bugs)

@app.route('/login',methods=['GET','POST'])
def login():	
	if request.method == 'POST':
		if request.form['username'] != 'admin':
			flash('Invalid username!')
		elif request.form['password'] != '123456':
			flash('Invalid password!')
		else:
			session['logged_in'] = True
			flash('Successfully login!')
			return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('logged_in',None) 
	return redirect(url_for('index'))

@app.route('/create',methods = ['POST','GET'])
def create():
	if request.method == 'POST':

		f = request.files['file']     #获取文件对象

		if not request.form['name']:
			flash('Bug name can not be empty.')
			return render_template('create.html')
		else :
			name = request.form['name']
			description = request.form['description']
			owner = request.form['owner']
			details = request.form['details']

			fname = secure_filename(f.filename)  #获取安全的文件名。f.filename是获取文件名，但这个值是可以伪造的
			f.save(os.path.join(upload_path, fname))   #以upload/111.jpg的形式保存文件到指定上传路径
			flash('Picture upload successfully.')

			g.db.bugs.insert({'name':name,'description':description,'owner':owner,'details':details,'filename':fname})   #这里的filename字段方便在页面访问文件。
			flash('Submmit success!')
			return redirect(url_for('index'))
	return render_template('create.html')

@app.route('/edit/<post_id>',methods = ['POST','GET'])
def edit(post_id):
	bug = g.db.bugs.find_one({'_id':ObjectId(post_id)})
	if not session.get('logged_in'):   #判断是否登录(logged_in 键在会话中存在，若已登录即为 True )
		flash('You should login first!')
		return redirect(url_for('index'))
	else:
		return render_template('edit.html',post=bug)

@app.route('/update',methods=['POST'])
def update():
	data = request.form.to_dict()
	f = request.files['file']     #上传的文件

	if not data['name']:
		flash('Bug name can not be empty.')
		return render_template('edit.html',post= data)
	else :
		fname = secure_filename(f.filename)
		f.save(os.path.join(upload_path, fname))
		flash('Picture upload successfully.')

		post_id = data.pop('id', None)
		g.db.bugs.update({'_id': ObjectId(post_id)}, data)
		flash('Edit success!')
		return redirect(url_for('index'))

@app.route('/delete/<post_id>',methods = ['POST','GET'])
def delete(post_id):
	if not session.get('logged_in'):   #判断是否登录(logged_in 键在会话中存在，若已登录即为 True )
		flash('You should login first!')
	else:
		g.db.bugs.remove({'_id':ObjectId(post_id)})
	return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded(filename):
	return send_from_directory(os.path.join('uploads',filename))


if __name__=='__main__':
	app.run()
