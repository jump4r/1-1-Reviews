from pprint import pprint
import parse
import praw
import config
import keywords
import sqlite3
import os
from review import Review
from post import Post

class Streamer:
    running = False

    def login(self):
        pprint('logging in')
        r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "WebApp:com.jump4r.1-1Reviews:v0.1.0 by (/u/jump4r")
        print ("logged in")
        running = True
        return r

    def stream_from_reddit(self, reddit):
        pprint('starting stream')
        subreddit = reddit.subreddit('jump4r')
        for submission in subreddit.stream.submissions():
            self.process_submission(submission)
        

    def process_submission(self, post):
        if "[review]" in post.title.lower():

            conn = sqlite3.connect('\\'.join([os.path.dirname(os.path.abspath(__file__)), 'replist.db']))
            c = conn.cursor()
            c.execute('SELECT * FROM posts WHERE uID = ?', ( post.id, ))
            if (c.fetchone() != None):
                print(post.title + ' is already in the database')
                c.close()
                conn.close()
                return False

            print(post.title + ' is not in the database, adding')
            split_selftext = post.selftext.split('\n')
            index, review_start_index, review_end_index = 0, -1, -1

            while (index < len(split_selftext)):
                if (review_start_index == review_end_index and "|" in split_selftext[index]):
                    review_start_index = index
                elif (review_start_index != review_end_index and "|" in split_selftext[index]):
                    review_end_index = index
                index += 1

            if (review_start_index == -1 or review_end_index == -1):
                return []

            r = parse.parse_review(split_selftext[review_start_index:review_end_index+1], post.author.name, post.created)
            p = Post(post.author.name, r, post.created, post.url, post.id)

            # Reply with bot/post info

streamer = Streamer()
reddit = streamer.login()
streamer.stream_from_reddit(reddit)