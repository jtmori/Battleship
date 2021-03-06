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
from application.game import game_logic

lst_server = []
lst_game = []
lst = [] # will contain the player's list 
lst1 = []
lst2 = []
lst3 = []

#rocket_list = [] # list of tuple containting opponent name and coordinates
aimed_move = []
move_response = []
game_status = 'ongoing'

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
				session['ships'] = lst
				session['hits'] = []
				session['misses'] = []
				session['hits_to_fleet'] = []
				session['misses_to_fleet'] = []
				session['RTR'] = False

				temp_board = game_logic.whip_up_new_board()

				# board is the bottom one in the page
				session['board'] = game_logic.add_ships_to_board(temp_board, lst)

				# opponent board is the top one in the page
				session['opponent_board'] = game_logic.whip_up_new_board()

				game_logic.game_start()
				pairs = homepage.get_pairs()
				user2 = ''
				for item in pairs:
					if session['username'] in item:
						lst = list(item)
						lst.remove(session['username'])
						user2 = lst[0]
						
				# saves opponent in session
				session['opponent'] = user2
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
				flash("These are not valid squares!  Repick! </br>")
	return render_template('game_setup.html')

@app.route('/game/', methods=['POST','GET'])
def game():
	global aimed_move
	global move_response
	global game_status
	if request.method == 'POST':
		if request.form['submit'] == 'Fire!':
			print("Inside FIRE")
			if session['RTR']:
				coord = str(request.form['Coordinate'])
				if len(coord) != 2:
					print("Not a valid move, please try another move!")
				else:
					print(coord, " is the coordinate being tried.")
					if game_logic.is_valid_move(coord):
						aimed_move = [session['opponent'],coord]
						print(session['username'], " is sending ", coord)
					else:
						flash("Not a valid move, please try another move!</br>")
			else:
				flash("Not your turn, please wait</br>")
		elif request.form['submit'] == 'Check for Attack':
			print("Inside CHECK FOR ATTACK")
			if not session['RTR']:
				if session['username'] in aimed_move:
					coord_recv = aimed_move[1]
					temp_boat_coords = session['ships']
					temp_misses = session['misses_to_fleet']
					temp_hits = session['hits_to_fleet']
					temp_board = session['board']
					for boat in temp_boat_coords:
						print(boat[0], " is the first item in the boat")
						if boat[0] == 'X':
							continue
						if coord_recv in boat:
							temp_hits.append(coord_recv)
							boat.remove(coord_recv)
							temp_board[game_logic.convert_from_number_to_int(coord_recv[1])][game_logic.convert_from_letter_to_int(coord_recv[0])] = 'O'
							print(session['opponent'], " hit!!")
							if boat[0] == 'X':
								print(session['opponent'], " has sunken a ship!")
								game_logic.print_board(temp_board)
							session['ships'] = temp_boat_coords
							session['hits_to_fleet'] = temp_hits
							move_response = [session['opponent'], 'Hit']
							break
						else:
							temp_misses.append(coord_recv)
							session['misses_to_fleet'] = temp_misses
							temp_board[game_logic.convert_from_number_to_int(coord_recv[1])][game_logic.convert_from_letter_to_int(coord_recv[0])] = 'X'
							move_response = [session['opponent'], 'Miss']
							print(session['opponent'], " missed!!")
						session['board'] = temp_board
					if game_logic.check_game_over(session['ships']):
						print('game should be over')
						session['WIN'] = False
						game_status = 'end'
						return redirect(url_for('loser'))
					
					session['RTR'] = True
		elif request.form['submit'] == 'Check for Response':
			print("CHECK FOR RESPONSE")
			if session['RTR']:
				if session['username'] in move_response:
					response = move_response[1]
					temp_board = session['opponent_board']
					coord = aimed_move[1]
					# X represents a miss, O (capital o, not zero) represents a hit
					#TODO: graphic logic
					if response == 'Miss':
						temp_board[game_logic.convert_from_number_to_int(coord[1])][game_logic.convert_from_letter_to_int(coord[0])] = 'X'
						session['misses'].append(aimed_move[1])
					else:
						temp_board[game_logic.convert_from_number_to_int(coord[1])][game_logic.convert_from_letter_to_int(coord[0])] = 'O'
						session['hits'].append(aimed_move[1])
					session['opponent_board'] = temp_board
					aimed_move = []
					move_response = []
					session['RTR'] = False
					if game_status == 'end':
						session['WIN'] = True
						return redirect(url_for('winner'))

	return render_template('game.html', user1 = session['username'], user2 = session['opponent'], opp_board = session['opponent_board'], board = session['board'])

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
	lst1 = [start1]
	lst2 = [start2]
	lst3 = [start3]

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
				print("Conflict found on coordinate ", coord)
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
	lst1.append('X')
	lst2.append('X')
	lst3.append('X')
	return True

# no longer using end_game
@app.route('/winner', methods=['POST','GET'])
def winner():
	session.pop('ships', None)
	session.pop('hits', None)
	session.pop('misses', None)
	session.pop('hits_to_fleet', None)
	session.pop('misses_to_fleet', None)
	session.pop('RTR', None)
	session.pop('board', None)
	session.pop('opponent_board', None)
	session.pop('opponent', None)
	if request.method == 'POST':
		if request.form['submit'] == 'Back To Home':
			return redirect(url_for('home_page'))
	return render_template('winner.html')

@app.route('/loser', methods=['POST','GET'])
def loser():
	session.pop('ships', None)
	session.pop('hits', None)
	session.pop('misses', None)
	session.pop('hits_to_fleet', None)
	session.pop('misses_to_fleet', None)
	session.pop('RTR', None)
	session.pop('board', None)
	session.pop('opponent_board', None)
	session.pop('opponent', None)
	if request.method == 'POST':
		if request.form['submit'] == 'Back To Home':
			return redirect(url_for('home_page'))
	return render_template('loser.html')
