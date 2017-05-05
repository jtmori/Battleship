from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
import threading
import time
import atexit

from application import app

#print("Login is running currently!")
#login_count = 0;

engine = create_engine('sqlite:///tutorial.db', echo=True)
# create a Session
#Session = sessionmaker(bind=engine)
#session = Session()

# class myThread (threading.Thread):
# 	def __init__(self, threadID, name):
# 		threading.Thread.__init__(self)
# 		self.threadID = threadID
# 		self.name = name
# 	def run(self):
# 		print("Starting ",self.name)
# 		print("Exiting ",self.name)

# def create_app():
# 	app = Flask(__name__)
# 	print("After app = FLASK")
	
# 	def interrupt():
# 		global thread
# 		thread.cancel()

# 	def doStuffStart():
# 		# Do initialisation stuff here
# 		global thread
# 		print("In DoStuffStart")
# 		# Create your thread
# 		time.sleep(5) 
# 		# TODO: Replace this with the Server Thread Code / Client Thread Code
# 		thread.start()

# 	doStuffStart()
# 	atexit.register(interrupt)
# 	return app

# thread = myThread(1, "tName1")
# app = create_app()
 
@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('logged_in.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
	if request.method == 'POST':
			if request.form['submit'] == 'Log in':
				POST_USERNAME = str(request.form['username'])
				POST_PASSWORD = str(request.form['password'])

				Session = sessionmaker(bind=engine)
				s = Session()
				query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
				result = query.first()
			
				if result:
					session['logged_in'] = True
					#login_count += 1;
					#print("Value for login_count is ", login_count)
					return render_template('logged_in.html')
				else:
					flash('wrong password!')
				return render_template('login.html')
			elif request.form['submit'] == 'New User':
				return render_template('new_account.html')
	return render_template('login.html')

@app.route('/new_account', methods=['POST'])
def make_new_account():
	#return render_template('new_account.html')
	if request.method == 'POST':
		if request.form['submit'] == 'Create Account':
			POST_USERNAME = str(request.form['username'])
			POST_PASSWORD = str(request.form['password'])
			Session = sessionmaker(bind=engine)
			s = Session()
			user = User(POST_USERNAME, POST_PASSWORD)
			s.add(user)
			s.commit()
			flash("Account Created")
			return render_template('new_account.html');
		elif request.form['submit'] == 'Back to Login':
			return render_template('login.html');
	return render_template('new_account.html')

#home page eventually - need to rename and replace the title/route/html file
@app.route('/logged_in', methods=['POST'])
def home_page():
	if session['logged_in'] == True:
		session['logged_in'] = False
		return render_template('login.html')
	return render_template('logged_in.html')

@app.route('/logout', methods=['POST'])
def do_admin_logout():
	if session['logged_in'] == True:
		session['logged_in'] = False
		return render_template('login.html')
	return render_template('logout.html')

if __name__ == "__main__":
	#app.secret_key = os.urandom(12)
	#app.config['CSRF_SESSION_KEY'] = os.urandom(24)
	#app.config['SECRET_KEY'] = os.urandom(12)

	PORT_NO = 125
	HOST = '127.0.0.1'
	print("Hello 1")
	app.run(debug=True,threaded=True)
	print("Hello 2")
