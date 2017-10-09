from django.shortcuts import render
from django.views.generic import TemplateView
import sys, os
sys.path.append("\\".join([os.path.dirname(__file__), "RepScraper"]))

from RepScraper import scraper
from .models import Post, Review
import sqlite3

class AppView(TemplateView):
    template_name = 'webapp/home.html'

    def get(self, request):
        #posts = scraper.scrape_reddit()
        p = scraper.scrape_reddit()
        """
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

        print('GET Request from User')
        c.close()
        conn.close() """

        return render(request, self.template_name, {"app_content": ["scraper.test", "test string 2"], "posts": Post.objects.all()})