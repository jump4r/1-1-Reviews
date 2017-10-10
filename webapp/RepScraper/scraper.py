from pprint import pprint
import os, sys, time
import django
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..\\..']))
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..']))
from RepReviews import settings

import parse, config, keywords
import praw

def login():
    r = praw.Reddit(username=config.username,
                password=config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "WebApp:com.jump4r.1-1Reviews:v0.1.0 by (/u/jump4r)")
    print ("logged in")
    return r

def get_reviews(reddit):
    try:
        from webapp.models import Post, Review
    except django.core.exceptions.AppRegistryNotReady:
        print('Cannot Load Models because the models are not ready')
        return False

    posts = []
    for post in reddit.subreddit("jump4r").hot(limit=10):
        if "[review]" in post.title.lower():
            
            try:
                p_exists = Post.objects.get(id=post.id)
                continue
            except Post.DoesNotExist:
                pass

            p = Post(user=post.author.name, date=post.created, link=post.url, id=post.id, title=post.title)
            p.save()
            
            pprint(('Post: ' + str(p)))
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

            r_list = parse.parse_review(split_selftext[review_start_index:review_end_index+1], p)
            for r in r_list:
                p.review_set.create(user=r.user, date=r.date, itemName=r.itemName, itemLink=r.itemLink, itemReview=r.itemReview, itemSize=r.itemSize)
        
    return posts

def scrape_reddit():
    
    reddit = login()
    return (get_reviews(reddit))


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepReviews.settings')
    django.setup()
    try:
        from webapp.models import Post, Review
        reddit_posts = scrape_reddit()

    except django.core.exceptions.AppRegistryNotReady:
        print('Cannot Load Models because the models are not ready')

    #update_database(reddit_posts)
    #print('calling streamer')
    #process = subprocess.Popen(['python', 'streamer.py'])
    #print("finished")