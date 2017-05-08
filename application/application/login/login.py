from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import datetime
from sqlalchemy.orm import sessionmaker
from tabledef import *
import threading
import time
import atexit

from application import app
from application.home import homepage
from application.game import game

# engine = create_engine('sqlite:///tutorial.db', echo=True)
login_count = 0;

 
def get_login_count():
	global login_count
	return login_count

def set_login_count(val):
	global login_count
	login_count = val

def decrement_login_count():
	global login_count
	login_count = login_count - 1

def increment_login_count():
	global login_count
	login_count = login_count + 1

def print_login_count():
	global login_count
	print(login_count," is the value of login_count")

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('homepage.html')

@app.route('/login', methods=['POST', 'GET'])
def do_login():
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
					session['username'] = POST_USERNAME
					print(session['username'], " is the user currently")
					session['logged_in'] = True
					login_count += 1
					print("Value for login_count is ", login_count)
					if(login_count == 2):
						print("Room full, game starts!")
						# logic for playing moved to homepage.py
					return redirect(url_for('home_page'))
				else:
					flash('wrong password!')
				return render_template('login.html')
			elif request.form['submit'] == 'New User':
				return render_template('new_account.html')
	return render_template('login.html')

@app.route('/new_account', methods=['POST', 'GET'])
def make_new_account():
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
			return redirect(url_for('do_login')) 
	return render_template('new_account.html')

# for when people try and circumvent some things
@app.route('/error_page', methods=['POST','GET'])
def get_error_page():
	if request.form['submit'] == 'Go to Login':
			return redirect(url_for('login')) 
	return render_template('error_page.html')
