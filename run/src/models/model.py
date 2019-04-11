from ..mappers.mapper import Database
import sqlite3
import time

class User:

    def __init__(self, username):
        self.username = username

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
        # TODO

    def signup(self, username, password, confirm):
        try:
            if password == confirm:
                with Database() as db:
                    db.cursor.execute('''INSERT INTO users (username, password)
                                        VALUES(?,?);''',
                                        (username, password))
                return True
        except sqlite3.IntegrityError:
            return False

    def login(self, password):
        with Database() as db:
            db.cursor.execute('''SELECT password FROM users WHERE username="{username}";'''
                .format(username=self.username))
            correct_password = db.cursor.fetchone()
            if correct_password is None:
                return False
            else:
                if correct_password[0] == password:
                    return True
                else:
                    return False

    def tweet(self, tweet):
        time_ = time.time()
        if len(tweet) < 240:
            with Database() as db: 
                db.cursor.execute('''INSERT INTO tweets (username, tweet, time)
                                    VALUES (?, ?, ?);''',
                                    (self.username, tweet, time_))
                return True
        else:
            return False

    def retweet(self, tweet_id):
        time_ = time.time()
        with Database() as db:
            db.cursor.execute('''SELECT username FROM tweets WHERE tweet_id={tweet_id};'''
                                .format(tweet_id = int(tweet_id)))
            retweeted_from = db.cursor.fetchone()
            db.cursor.execute('''SELECT tweet FROM tweets WHERE tweet_id={tweet_id};'''
                                .format(tweet_id = int(tweet_id)))
            text = db.cursor.fetchone()
            db.cursor.execute('''SELECT likes FROM tweets WHERE tweet_id={tweet_id};'''
                                .format(tweet_id = int(tweet_id)))
            likes = db.cursor.fetchone()
            db.cursor.execute('''SELECT retweets FROM tweets WHERE tweet_id={tweet_id};'''
                                .format(tweet_id = int(tweet_id)))
            retweets = db.cursor.fetchone()
            db.cursor.execute('''UPDATE tweets SET retweets = retweets + 1 WHERE tweet_id={tweet_id};'''
                                .format(tweet_id = int(tweet_id)))
            retweet = "@" + (retweeted_from[0]) + ': "' + (text[0]) + '"'
            db.cursor.execute('''INSERT INTO tweets (username, tweet, time, likes, retweets)
                                    VALUES (?, ?, ?, ?, ?);''',
                                    (self.username, retweet, time_,int(likes[0]),int(retweets[0])+1))
            return True

    def like(self, tweet_id):
        with Database() as db:    
            db.cursor.execute('''UPDATE tweets SET likes = likes + 1 WHERE tweet_id={tweet_id};'''
                                .format(tweet_id = int(tweet_id)))
            return True

    def user_tweets(self):
        with Database() as db:
            db.cursor.execute('''SELECT * FROM tweets WHERE username='{username}' ORDER BY time DESC;'''
                    .format(username = self.username))
            user_tweets = db.cursor.fetchall()
            return user_tweets


class Tweets:

    def __init__(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
        # TODO

    def alltweets(self):
        with Database() as db:
            db.cursor.execute('''SELECT * FROM tweets ORDER BY time DESC;''')
            alltweets = db.cursor.fetchall()
            return alltweets