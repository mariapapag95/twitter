from flask import Blueprint, render_template, request, session, redirect, url_for
from ..models.model import User, Tweets

controller = Blueprint('public',__name__)

@controller.route('/')
def frontpage():
    return render_template('home.html')

@controller.route('/public', methods=['GET'])
def dashboard():
    t = Tweets()
    alltweets = t.alltweets()
    if request.method == 'GET':
        return render_template('public.html', alltweets=alltweets)

@controller.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        u = User(username)
        if u.signup(username, password, confirm):  
            session["username"] = username  
            return redirect(url_for('private.dashboard'))
        else:
            error = 'That username is already taken. Choose another.'
            return render_template('signup.html', message=error)

@controller.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = User(username)
        if u.login(password):
            session["username"] = username  
            return redirect(url_for('private.dashboard'))
        else:
            error = "Username or password inccorect. Try again."
            return render_template('login.html', message=error)

"""
@controller.route('/<username>',methods=['GET','POST'])
def userpage():
    pass
"""