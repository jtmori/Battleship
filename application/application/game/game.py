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

usernames_in_room = []

@app.route('/game/', methods=['POST','GET'])
def game():
	if not session.get('logged_in'):
		return redirect(url_for('error_page'))
	print("Game service activated!")
	usernames_in_room.append(session['username'])
	print("Size of usernames_in_room is ", len(usernames_in_room))
	# while(len(usernames_in_room) != 2):
	# 	time.sleep(1)
	if usernames_in_room.index(session['username']) == 0:
		return render_template('game.html', user1 = session['username'], user2 = usernames_in_room[1])
	else:
		return render_template('game.html', user1 = session['username'], user2 = usernames_in_room[0])
	