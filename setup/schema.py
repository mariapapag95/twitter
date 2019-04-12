import sqlite3

connection = sqlite3.connect('setup/twitter.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE, 
    password VARCHAR
    );''')

cursor.execute('''CREATE TABLE tweets(
    tweet_id INTEGER PRIMARY KEY,
    username VARCHAR,
    tweet VARCHAR,
    retweeted_from VARCHAR, 
    original_tweet_id INTEGER,
    original_poster INTEGER,
    time VARCHAR,
    likes INTEGER DEFAULT '0',
    retweets INTEGER DEFAULT '0',
    FOREIGN KEY (username) REFERENCES users(username)
    FOREIGN KEY (retweeted_from) REFERENCES users(username)
    FOREIGN KEY (original_poster) REFERENCES users(username)
    );''')

cursor.execute('''CREATE TABLE retweets(
    retweet_id INTEGER PRIMARY KEY,
    user_who_retweeted VARCHAR, 
    tweet_id VARCHAR,
    time VARCHAR,
    FOREIGN KEY (user_who_retweeted) REFERENCES users(username),
    FOREIGN KEY (tweet_id) REFERENCES tweets(original_tweet_id)
    );''')    

cursor.execute('''CREATE TABLE likes(
    like_id INTEGER PRIMARY KEY,
    user_who_liked VARCHAR, 
    tweet_id VARCHAR,
    time VARCHAR,
    FOREIGN KEY (user_who_liked) REFERENCES users(username),
    FOREIGN KEY (tweet_id) REFERENCES tweets(original_tweet_id)
    );''')    

connection.commit()
cursor.close()



"""
cursor.execute('''CREATE TABLE retweets(
    retweet_id INTEGER PRIMARY KEY,
    original_id INTEGER,
    retweeter VARCHAR, 
    op VARCHAR,
    tweet VARCHAR,
    time VARCHAR,
    likes INTEGER,
    retweets INTEGER,
    FOREIGN KEY (op) REFERENCES users(username),
    FOREIGN KEY (tweet) REFERENCES tweets(tweet),
    FOREIGN KEY (likes) REFERENCES tweets(likes),
    FOREIGN KEY (retweets) REFERENCES tweets(retweets),
    FOREIGN KEY (original_id) REFERENCES tweets(tweet_id)
    );''')
"""
