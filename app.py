from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite://tutorial.db', echo=True)
 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('logout.html')

@app.route('/logout', methods=['POST'])
def do_admin_logout():
    if session['logged_in'] == True:
        session['logged_in'] = False
        return home()
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/test')
def test():
 
    POST_USERNAME = "python"
    POST_PASSWORD = "python"
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        return "Object found"
    else:
        return "Object not found " + POST_USERNAME + " " + POST_PASSWORD
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)