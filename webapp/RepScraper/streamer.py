from pprint import pprint
import django
import sys, os
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..\\..']))
sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), '..']))
import parse, config, keywords
import praw
import threading

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
        print('Post Recieved')
        if "[review]" in post.title.lower():

            try:
                p_exists = Post.objects.get(id=post.id)
                return False
            except Post.DoesNotExist:
                pass

            p = Post(user=post.author.name, date=post.created, link=post.url, id=post.id, title=post.title)
            p.save()

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
            for r in r_list:
                r.save()


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepReviews.settings')
    django.setup()

    try:
        from webapp.models import Post, Review
        streamer = Streamer()
        reddit = streamer.login()
        stream_thread = threading.Thread(target=streamer.stream_from_reddit, args=(reddit, ))
        stream_thread.start()
        
    except django.core.exceptions.AppRegistryNotReady:
        print('Cannot Load Models because the models are not ready')

    print('We are in the best thread')

#streamer = Streamer()
#reddit = streamer.login()
#streamer.stream_from_reddit(reddit)