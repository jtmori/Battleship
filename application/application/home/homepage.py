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
from application.game import game

room_open = False;

pairs = []
opponents = []
all_players = []
#queue system for playing
#ready to play, click button, put into opponents
#can view list of opponents who aren't you
#when click play, you're removed for list
#replace the logic for login_count

def get_pairs():
	global pairs
	return pairs

def print_room_open_value():
	global room_open
	if room_open == True:
		print("Value of room_open is True")
	else:
		print("Value of room_open is False")

#homepage - used to start game
@app.route('/home/', methods=['POST', 'GET'])
def home_page():
	global room_open
	global all_players
	global opponents
	global pairs
	if not session['username'] in all_players:
		all_players.append(session['username'])

	if request.method == 'POST':
		print("POST being called")
		#logout - redirects to do_login; html has /login
		if request.form['submit'] == 'Log Out':
			if session['logged_in']:
				login_count = login.get_login_count()
				login_count = login_count - 1
				session['logged_in'] = False
				opponents.pop(session['username'])
				#update pairs tuples when someone logs out
				for item in pairs:
					if session['username'] in item:
						lst = list(item)
						pairs.remove(item)
						lst.remove(session['username'])
						if len(opponents) >=1:
							lst.append(opponents.pop())
							pairs.append(tuple(lst))

				session.pop('usernname', None)
				login.set_login_count(login_count)
				return redirect(url_for('do_login'))

		#ready to play - adds user to opponents list; html has /home/
		elif request.form['submit'] == 'Ready To Play':
			if not session['username'] in opponents:
				opponents.append(session['username'])
				print("List of opponents: ")
				for item in opponents:
					print(item)
				return render_template('homepage.html')

		#play game -redirects to game in game.py; html has /home/
		elif request.form['submit'] == 'Play Game':
			for item in pairs:
				if session['username'] in item:
					session['tuple'] = item
					return redirect(url_for('game'))
			if len(opponents) >= 2:
				opponents.remove(session['username'])
				tup = (session['username'], opponents.pop())
				pairs.append(tup)
				print("List of pair tuples: ")
				for item in pairs:
					for i in item:
						print(i)
					print()
				session['tuple'] = tup
				return redirect(url_for('game'))

			# if room_open == True:
			# 	print("Joining Room and Setting room_open to False")
			# 	login.decrement_login_count()
			# 	login.print_login_count()
			# 	room_open = False
			# 	return redirect(url_for('game'))
			# elif login_count >= 2:
			# 	room_open = True
			# 	login.decrement_login_count()
			# 	login.print_login_count()
			# 	return redirect(url_for('game'))

			#if not enough opponents yet
			else:
				login.print_login_count()
				return render_template('homepage.html')

		#if not logged in, gets error page to login; html has /login
		elif request.form['submit'] == 'Login':
			print("In error page")
			return redirect(url_for('do_login'))
	return render_template('homepage.html')


