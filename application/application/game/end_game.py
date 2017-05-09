from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
import threading
import time
import atexit
from random import randint

from application import app
from application.login import login
from application.home import homepage
from application.game import game_logic, game

@app.route('/winner', methods=['POST','GET'])
def winner():
	#session.pop('ships', None)
	#session.pop('hits', None)
	#session.pop('misses', None)
	#session.pop('hits_to_fleet', None)
	#session.pop('misses_to_fleet', None)
	#session.pop('RTR', None)
	#session.pop('board', None)
	#session.pop('opponent_board', None)
	#session.pop('opponents', None)
	if request.form['submit'] == 'Back To Home':
		return redirect(url_for('home_page'))
	return render_template('winner.html')

@app.route('/loser', methods=['POST','GET'])
def loser():
	#session.pop('ships', None)
	#session.pop('hits', None)
	#session.pop('misses', None)
	#session.pop('hits_to_fleet', None)
	#session.pop('misses_to_fleet', None)
	#session.pop('RTR', None)
	#session.pop('board', None)
	#session.pop('opponent_board', None)
	#session.pop('opponents', None)
	if request.form['submit'] == 'Back To Home':
		return redirect(url_for('home_page'))
	return render_template('loser.html')