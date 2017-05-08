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
from application.home import homepage



@app.route('/game/', methods=['POST','GET'])
def game():
	pairs = homepage.get_pairs()
	user1 = session['username']
	if not session.get('logged_in'):
		return redirect(url_for('error_page'))
	print("Game service activated!")
	user2 = ''
	for item in pairs:
		if session['username'] in item:
			lst = list(item)
			lst.remove(session['username'])
			user2 = lst[0]
			print(user2, "is the other user")
	return render_template('game.html', user1 = session['username'], user2 = user2)