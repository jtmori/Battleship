from flask import Flask, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading
import time
import os
import atexit

engine = create_engine('sqlite:///tutorial.db', echo=True)

class myThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		print("Starting ",self.name)
		print("Exiting ",self.name)

def create_app():
	app = Flask(__name__)
	print("After app = FLASK")
	
	def interrupt():
		global thread
		thread.cancel()

	def doStuffStart():
		# Do initialisation stuff here
		global thread
		print("In DoStuffStart")
		# Create your thread
		time.sleep(5) 
		# TODO: Replace this with the Server Thread Code / Client Thread Code
		thread.start()

	doStuffStart()
	atexit.register(interrupt)
	return app

thread = myThread(1, "tName1")
app = create_app()
app.secret_key = os.urandom(12)

import application.login.login
import application.home.homepage
import application.game.game

if __name__ == "__main__":
	PORT_NO = 125
	HOST = '127.0.0.1'
	print("Hello 1")
	app.run(debug=True,threaded=True)
	print("Hello 2")