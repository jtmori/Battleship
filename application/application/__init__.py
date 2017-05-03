from flask import Flask
import threading
import time
import atexit

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

app = create_app()
thread = myThread(1, "tName1")

import application.myapp

