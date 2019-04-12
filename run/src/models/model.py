from ..mappers.mapper import Database
import sqlite3
import datetime

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
        time_ = datetime.datetime.now()
        time_ = time_.strftime("%c")
        if len(tweet) < 240:
            with Database() as db: 
                db.cursor.execute('''INSERT INTO tweets (username, tweet, original_poster, time)
                                    VALUES (?, ?, ?, ?);''',
                                    (self.username, tweet, self.username, time_))
                db.cursor.execute('''UPDATE tweets SET original_tweet_id = tweet_id WHERE tweet = "{tweet}";'''
                                    .format(tweet = tweet))
                return True
        else:
            return False

    def retweet(self, tweet_id):
        time_ = datetime.datetime.now()
        time_ = time_.strftime("%c")
        with Database() as db:
            # UPDATE RETWEETS OF ORIGINAL TWEET AND THE RETWEETED TWEET
            db.cursor.execute('''UPDATE tweets SET retweets = retweets + 1 WHERE tweet_id={tweet_id};'''
                                    .format(tweet_id = int(tweet_id)))
            # GET DATA OF TWEET YOU ARE RETWEETING
            db.cursor.execute('''SELECT * FROM tweets WHERE tweet_id={tweet_id};'''
                                .format(tweet_id = int(tweet_id)))
            tweet = db.cursor.fetchall()
            tweet = tweet[0]
            db.cursor.execute('''INSERT INTO retweets (user_who_retweeted, tweet_id, time)
                                    VALUES(?,?,?);''',
                                    (self.username, tweet[4], time_))
            if tweet[3] == None:
                # RETWEETING AN ORIGINAL TWEET
                db.cursor.execute('''INSERT INTO tweets (username, tweet, retweeted_from, original_tweet_id, original_poster, time, likes, retweets)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                                        (self.username, '"'+tweet[2]+'"', tweet[1], tweet[0], tweet[1], time_, tweet[7], tweet[8]))
                return True
            else: 
                # RETWEETING A RETWEET
                db.cursor.execute('''INSERT INTO tweets (username, tweet, retweeted_from, original_tweet_id, original_poster, time, likes, retweets)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                                        (self.username, tweet[2], tweet[1], tweet[4], tweet[5], time_, tweet[7], tweet[8]))
                db.cursor.execute('''UPDATE tweets SET retweets = {retweets} WHERE tweet_id = {original_tweet_id};'''
                                    .format(retweets = tweet[8], original_tweet_id = tweet[4]))
                return True

    def like(self, tweet_id):
        time_ = datetime.datetime.now()
        time_ = time_.strftime("%c")
        # NEEDS TO UPDATE LIKES ON ORIGINAL TWEET AS WELL
        # SELECT USING THE TWEET ID TO FIND THE ORIGINAL ID
        # THEN UPDATE WHERE ORIGINALID = ORIGINALID
        with Database() as db:
            db.cursor.execute('''SELECT original_tweet_id FROM tweets WHERE tweet_id={tweet_id};'''
                                .format(tweet_id = int(tweet_id)))
            original_tweet_id = db.cursor.fetchone()
            db.cursor.execute('''INSERT INTO likes (user_who_liked, tweet_id, time)
                                    VALUES(?,?,?);''',
                                    (self.username, original_tweet_id[0], time_))
            db.cursor.execute('''UPDATE tweets SET likes = likes + 1 WHERE original_tweet_id={original_tweet_id};'''
                                .format(original_tweet_id = int(original_tweet_id[0])))
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