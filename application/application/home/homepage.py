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
from application.login import login

room_open = False;

def print_room_open_value():
	global room_open
	if room_open == True:
		print("Value of room_open is True")
	else:
		print("Value of room_open is False")

@app.route('/home/', methods=['POST', 'GET'])
def home_page():
	global room_open
	print ("In homepage function")
	print (room_open, " is the value of room_open at start of home_page")
	print (login.get_login_count(), "is the login count")
	if request.method == 'POST':
		print("POST being called")
		if request.form['submit'] == 'Log Out':
			print("Log Out has been submitted.")
			if session['logged_in']:
				print('Session-logged_in value is True, hence this')
				login_count = login.get_login_count()
				login_count = login_count - 1
				print("login_count is", login_count)
				session['logged_in'] = False
				login.set_login_count(login_count)
				return redirect(url_for('do_login'))
		elif request.form['submit'] == 'Play Game': #adding this
			print("Play Game has been submitted.")
			login_count = login.get_login_count()
			print(login_count, " is the value of login_count after Play Game submitted")
			if room_open == True:
				print("Joining Room and Setting room_open to False")
				login.decrement_login_count()
				login.print_login_count()
				room_open = False
				return redirect(url_for('game'))
			elif login_count >= 2:
				room_open = True
				login.decrement_login_count()
				login.print_login_count()
				return redirect(url_for('game'))
			else:
				login.print_login_count()
				return render_template('homepage.html')
	return render_template('homepage.html')

@app.route('/game/', methods=['POST','GET'])
def game():
	if not session.get('logged_in'):
		return redirect(url_for('error_page'))
	print("Game service activated!")
	return render_template('game.html')
	
	#if request.method == 'POST':
	#	if request.form['submit']:

