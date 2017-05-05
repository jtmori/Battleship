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

print("login is running currently!") # proof that this is running, not login.py
login_count = 0;

engine = create_engine('sqlite:///tutorial.db', echo=True)
 
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
					global login_count
					if(login_count == 2):
						print("Two people already in room, login rejected")
						session['logged_in'] = False
						return render_template('room_full.html')
					session['logged_in'] = True
					login_count += 1
					print("Value for login_count is ", login_count)
					if(login_count == 2):
						print("Room full, game starts!")
						# logic for playing

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
	#print("No, this is logout!")
	if session['logged_in'] == True:
		global login_count
		login_count = login_count - 1	
		print("login_count is", login_count)
		session['logged_in'] = False
		return render_template('login.html')
	return render_template('logged_in.html')

@app.route('/logout', methods=['POST'])
def do_admin_logout():
	#print("This is logout")
	if session['logged_in'] == True:
		global login_count
		login_count = login_count - 1
		print("login_count is", login_count)
		session['logged_in'] = False
		return render_template('login.html')
	return render_template('logout.html')

if __name__ == "__main__":
	PORT_NO = 125
	HOST = '127.0.0.1'
	print("Hello 1")
	app.run(debug=True,threaded=True)
	print("Hello 2")
