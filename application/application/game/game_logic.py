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
from application.game import game, end_game

# checks if move is valid
def is_valid_move(coord):
	valid_row_list = ['A','B','C','D','E','F','G','H','I','J']
	valid_col_list = ['0','1','2','3','4','5','6','7','8','9']

	if coord[0] not in valid_row_list:
		print("Not a valid move, try again!")
		return False
	if coord[1] not in valid_col_list:
		print("Not a valid move, try again!")
		return False

	if coord in session['hits'] or coord in session['misses']:
		print("Move has already been tried, try again!")
		return False
	print("Valid move, executing!")
	return True

# used to define who goes first,
def game_start():
	pairs = homepage.get_pairs() # what is the order of get pair
	user1 = ''
	user2 = ''
	for item in pairs:
		if session['username'] in item:
			lst = list(item)
			user1 = lst[0]
			user2 = lst[1]
	decider = 1 # could generate a diff value for each, order should be same for both, right?
	if lst[decider] == session['username']:
		session['RTR'] = True
		print('RTR awarded to ', session['username'], ' ', session['RTR'])

def check_game_over(ships):
	for item in ships:
		if item[0] != 'X':
			return False
	return True

def print_board(board):
	for x in range(10):
		for y in range(10):
			print(board[x][y],end='')
		print()

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