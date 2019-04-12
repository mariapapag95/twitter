from flask import Blueprint, render_template, request, session, redirect, url_for
from ..models.model import User, Tweets

controller = Blueprint('private',__name__)

@controller.route('/dashboard', methods=['GET','POST'])
def dashboard():
    t = Tweets()
    alltweets = t.alltweets()
    if request.method == 'GET':
        return render_template('dashboard.html', alltweets=alltweets)
    elif request.method == 'POST':
        try:
            tweet = request.form.get('tweet')
            retweet = request.form.get('retweet')
            like = request.form.get('like')
            u = User(session["username"])
            if retweet:
                if u.retweet(retweet):
                    return redirect(url_for('private.dashboard'))
            if like:
                if u.like(like):
                    return redirect(url_for('private.dashboard'))
            if u.tweet(tweet):
                return redirect(url_for('private.dashboard'))
            else:
                message = "Your tweet is too long. Character limit 240."
                return render_template('dashboard.html', alltweets=alltweets, message=message)      
        # HANDLES FOR PEOPLE TRYING TO TWEET WHEN THEY ARE NOT LOGGED IN
        # FIXME: CREATE JINJA CONDITION TO NOT DISPLAY INPUT BOX UNLESS THE USER IS LOGGED IN (SESSION DATA)
        except KeyError:
            return redirect(url_for('public.frontpage'))

@controller.route('/user', methods=['GET','POST'])
def mypage():
    u = User(session["username"])
    user_tweets = u.user_tweets()   
    if request.method == 'GET':
        return render_template('user.html', user_tweets = user_tweets,username = user_tweets[0][1])    
    elif request.method == 'POST': 
        try:
            tweet = request.form.get('tweet')
            retweet = request.form.get('retweet')
            like = request.form.get('like')
            if retweet:
                if u.retweet(retweet):
                    return redirect(url_for('private.mypage'))
            if like:
                if u.like(like):
                    return redirect(url_for('private.mypage'))
            if u.tweet(tweet):
                return redirect(url_for('private.mypage'))
            else:
                message = "Your tweet is too long. Character limit 240."
                return render_template('user.html', user_tweets = user_tweets,message=message)    
    # HANDLES FOR PEOPLE TRYING TO TWEET WHENT THEY ARE NOT LOGGED IN
    # FIXME: CREATE JINJA CONDITION TO NOT DISPLAY INPUT BOX UNLESS THE USER IS LOGGED IN (SESSION DATA)
        except KeyError:
            return redirect(url_for('private.frontpage'))


# I WANT THE USER PAGE (INCLUDING MY TWAT) TO BE "/<USERNAME>""


@controller.route('/logout',methods=['GET'])
def logout():
    try:
        if request.method == 'GET':
            session.pop('username') 
            return render_template('logout.html')
    except KeyError:
        return render_template('logout.html')
