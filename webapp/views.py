from django.shortcuts import render
from django.views.generic import TemplateView
import sys, os
sys.path.append("\\".join([os.path.dirname(os.path.abspath(__file__)), "RepScraper"]))
from .models import Post, Review

class ViewPost:
    def __init__(self, post, reviews):
        self.post = post
        self.reviews = reviews

    def filter(self, filter):
        pass

class AppView(TemplateView):
    template_name = 'webapp/home.html'

    def get(self, request):
        #posts = scraper.scrape_reddit()
        print('GET Request Recieved')

        return render(request, self.template_name, {"app_content": ["scraper.test", "test string 2"], "posts": Post.objects.all()})