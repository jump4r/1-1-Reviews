from pprint import pprint
import parse
import praw
import config
import keywords
import sqlite3
import os
from review import Review
from post import Post
import subprocess

def login():
    r = praw.Reddit(username=config.username,
                password=config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "WebApp:com.jump4r.1-1Reviews:v0.1.0 by (/u/jump4r")
    print ("logged in")
    return r

def get_reviews(reddit):
    posts = []
    for post in reddit.subreddit("jump4r").hot(limit=2):
        if "[review]" in post.title.lower():
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
            
            if (r):
                p = Post(post.author.name, r, post.created, post.url, post.id)
                pprint((p.user, p.date, p.link, p.id))
                posts.append(p)

    return posts

def scrape_reddit():
    reddit = login()
    return (get_reviews(reddit))


def update_database(posts):
    path = '\\'.join([os.path.dirname(__file__), 'replist.db'])
    print(path)
    conn = sqlite3.connect(path)
    c = conn.cursor()

    for post in posts:
        c.execute("INSERT INTO posts (user, date, link, uID) VALUES (?, ?, ?, ?)", (post.user, post.date, post.link, post.id))

        for review in post.reviews:
            c.execute("INSERT INTO reviews (user, date, itemName, itemLink, itemReview, uID, itemSize) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (post.user, post.date, review.name, review.link, review.review, review.postId, review.size))

    conn.commit()
    c.close()
    conn.close()

#reddit_posts = scrape_reddit()
#update_database(reddit_posts)
#print('calling streamer')
#process = subprocess.Popen(['python', 'streamer.py'])
#print("finished")