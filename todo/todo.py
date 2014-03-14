#coding=utf-8
from flask import Flask,request,redirect,render_template,g,url_for
from pymongo import Connection
from bson.objectid import ObjectId

app = Flask(__name__)
app.debug = True


@app.before_request
def before_request():
	conn = Connection()
	g.db = conn.ttt
	
def get_lists():
	return g.db.list.find()


@app.route('/',methods=['POST','GET'])
def index():
	lis = get_lists()
	if request.method == 'POST':
		if request.form['content']:
			con = request.form['content']
			g.db.list.insert({'content':con})
			return redirect(url_for('index'))
		else:
			return "亲，内容不能为空哦"

	return render_template('todo.html', lists = lis)

@app.route('/delete/<todo_id>')
def delete(todo_id):
	g.db.list.remove({'_id': ObjectId(todo_id)})
	return redirect(url_for('index'))


if __name__=='__main__':
	app.run()