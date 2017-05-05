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
from application.login import login


@app.route('/home/', methods=['POST', 'GET'])
def home_page():
	if request.method == 'POST':
		if request.form['submit'] == 'Log out':
			if session['logged_in'] == True:
				global login_count
				login_count = login_count - 1
				print("login_count is", login_count)
				session['logged_in'] = False
				return redirect(url_for('login'))
	return render_template('homepage.html')