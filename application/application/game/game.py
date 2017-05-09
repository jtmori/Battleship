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

lst_server = []
lst_game = []
lst = [] # will contain the player's list 
lst1 = []
lst2 = []
lst3 = []

@app.route('/game_setup/', methods=['POST','GET'])
def game_setup():
	global lst1
	global lst2
	global lst3
	if request.method == 'POST':
		print("Inside Post of game_setup")
		if request.form['submit'] == 'Play':
			START1 = str(request.form['Boat 1'])
			DIR1 = str(request.form['Dir 1'])
			START2 = str(request.form['Boat 2'])
			DIR2 = str(request.form['Dir 2'])
			START3 = str(request.form['Boat 3'])
			DIR3 = str(request.form['Dir 3'])
			print(START1, " is START1")
			print(DIR2, " is DIR2")

			if check_if_valid_squares(START1,DIR1,START2,DIR2,START3,DIR3):
				print("These are valid squares!")
				lst = [] # no longer using global lst
				global lst_game

				# make lst contain player's coordinates
				lst.append(lst1)
				lst.append(lst2)
				lst.append(lst3)
				
				# adds your coordinates (for checks with enemy attempts)
				# and blank lists for hits and misses for the game about to play
				# RTR will say if it is your turn or theirs, both are by default false
				session(['your_ships']) = lst
				session(['your_hits']) = []
				session(['your_misses']) = []
				session(['RTR']) = False

				pairs = homepage.get_pairs()
				user2 = ''
				for item in pairs:
					if session['username'] in item:
						lst = list(item)
						lst.remove(session['username'])
						user2 = lst[0]
						
				# saves opponent in session
				session(['opponent']) = user2
				print(session['opponent'], 'is the other user, huzzah!')

				lst.append(session['username'])

				# currently assumes playing that one game, two games are not going to overlap each other
				lst_game.append(lst)

				lst1 = []
				lst2 = []
				lst3 = []

				if len(lst_game) == 2:
					lst_server.append(lst_game)
					lst_game = [] # empties it after adding to server
					# need to remember to remove it 
				return redirect(url_for('game'))
			else:
				
				lst1 = []
				lst2 = []
				lst3 = []
				flash("These are not valid squares!  Repick!")
	return render_template('game_setup.html')

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

# assumes a 10 by 10 board
# direction value of 0 is vertical, 1 is horizontal
# working as intended - need to recheck after using globals
def check_if_valid_squares(start1,dir1,start2,dir2,start3,dir3):
	print(start1, " is start1")
	print(dir1, " is dir1")
	print(start2, " is start2")
	print(dir2, " is dir2")
	print(start3, " is start3")
	print(dir3, " is dir3")
	if len(start1) != 2 or len(start2) != 2 or len(start3) != 2:
		print("Start square length parameters incorrect")
		return False
	valid_row_list = ['A','B','C','D','E','F','G','H','I','J']
	valid_col_list = ['0','1','2','3','4','5','6','7','8','9']

	if start1[0] not in valid_row_list or start2[0] not in valid_row_list or start3[0] not in valid_row_list:
		print("Rows do not properly match!")
		return False
	if start1[1] not in valid_col_list or start2[1] not in valid_col_list or start3[1] not in valid_col_list:
		print("Columns do not properly match!")
		return False

	if not (dir1 == '0' or dir1 == '1') or not (dir2 == '0' or dir2 == '1') or not (dir3 == '0' or dir3 == '1'):
		print("Directions not properly matching!")
		return False

	if start1 == start2 or start1 == start3 or start2 == start3:
		print("Same start square cannot be used for multiple boats")
		return False

	#no longer uses global of lst
	global lst1
	global lst2
	global lst3

	lst = [start1,start2,start3]
	lst1 = ['X',start1]
	lst2 = ['X',start2]
	lst3 = ['X',start3]

	# Checking for no overlap
	# Boat 1
	for x in range(1,3):
		# horizontal
		if dir1 == '1':
			coord = start1[0] + chr(ord(start1[1]) + x)
			if coord[1] == ':':
				print("Out of bounds on coord ", coord, ", too far right")
				return False
			lst1.append(coord)
			if coord in lst:
				print("Conflict found on coordinate ", coord)
				return False
			lst.append(coord)
		#vertical
		elif dir1 == '0':
			coord = chr(ord(start1[0]) + x) + start1[1]
			if chr(ord(coord[0])) > 'J':
				print("Out of bounds on coord ", coord)
				return False
			lst1.append(coord)
			if coord in lst:
				print("Conflict found on coordinate ", coord)
				return False
			lst.append(coord)

	# Boat 2
	for x in range(1,3):
		if dir2 == '1':
			coord = start2[0] + chr(ord(start2[1]) + x)
			if coord[1] == ':':
				print("Out of bounds on coord ", coord, ", too far right")
				return False
			lst2.append(coord)
			if coord in lst:
				flash("Conflict found on coordinate ", coord)
				return False
			lst.append(coord)
		elif dir2 == '0':
			coord = chr(ord(start2[0]) + x) + start2[1]
			if chr(ord(coord[0])) > 'J':
				print("Out of bounds on coord ", coord)
				return False
			lst2.append(coord)
			if coord in lst:
				print("Conflict found on coordinate ", coord)
				return False
			lst.append(coord)

	# Boat 3
	for x in range(1,3):
		if dir3 == '1':
			coord = start3[0] + chr(ord(start3[1]) + x)
			if coord[1] == ':':
				print("Out of bounds on coord ", coord, ", too far right")
				return False
			lst3.append(coord)
			if coord in lst:
				print("Conflict found on coordinate ", coord)
				return False
			lst.append(coord)
		elif dir3 == '0':
			coord = chr(ord(start3[0]) + x) + start3[1]
			if chr(ord(coord[0])) > 'J':
				print("Out of bounds on coord ", coord)
				return False
			lst3.append(coord)
			if coord in lst:
				print("Conflict found on coordinate ", coord)
				return False
			lst.append(coord)

	return True

# used to define who goes first,
def game_start():
	pairs = homepage.get_pairs() # what is the order of get pair
	user1 = ''
	user2 = ''
	if session['username'] in item:
		lst = list(item)
		user1 = lst[0]
		user2 = lst[1]
	decider = 1 # could generate a diff value for each, order should be same for both, right?
	if lst[decider] == session['username']:
		session['RTR'] = True
		print('RTR awarded to ', session['username'])


# used to make a board
def whip_up_new_board():
	board = [['-' for x in range(10)] for y in range(10)] 
	return board

# converts capital letter into int
def convert_from_letter_to_int(character):
	return ord(character) - 65 # 65 is 'A'

# converts number char into int
def convert_from_number_to_int(character):
	return ord(character) - 48