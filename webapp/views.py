from django.shortcuts import render
import sys, os
sys.path.append("\\".join([os.path.dirname(__file__), "RepScraper"]))
import scraper
from post import Post
from review import Review
import sqlite3

# Create your views here.
def index(request):
    #posts = scraper.scrape_reddit()
    posts = []
    conn = sqlite3.connect('\\'.join([os.path.dirname(__file__), 'RepScraper\\replist.db']))
    c = conn.cursor()

    # POST.tb = {user, date, link, uId}
    c.execute("SELECT * FROM posts")
    db_posts = c.fetchall()
    for row in db_posts:
        p = Post(row[0], [], row[1], row[2], row[3])
        c.execute("SELECT * FROM reviews WHERE uID = '%s'" %p.id)
        db_reviews = c.fetchall()
        reviews = []
        for r_row in db_reviews:
            # REVIEW.tb = {user, date, itemName, itemLInk, itemReview, uID, size}
            reviews.append(Review(r_row[0], r_row[1], r_row[2], r_row[3], r_row[4], r_row[6])) #I'm the literal worst

        p.reviews = reviews
        posts.append(p)

    print('check is this even working?')
    c.close()
    conn.close()

    return render(request, "webapp/home.html", {"app_content": ["scraper.test", "test string 2"], "posts": posts})