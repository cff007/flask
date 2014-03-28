from pymongo import Connection
from flask import Flask,g,render_template,request,flash,url_for,redirect
from bson.objectid import ObjectId

app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
	conn = Connection()
	g.db = conn.bugbank

def add(name,description,owner,details,picture):
	return g.db.bugs.inert({'name':name;'description':description;'owner':owner;'details':details;'picture':picture})

def delete(post_id):
	return g.db.bugs.remove({'_id':ObjectId(post_id)})

@app.route('/',method=['POST', 'GET'])
def index():
	


if __name__='__main__':
	app.run()
