from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
	return  'hello world!'

@app.route('/students')
def students():
	return 'hahah nima'

if __name__=='__main__':
	app.run()