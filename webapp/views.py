from django.shortcuts import render
from django.views.generic import TemplateView
import sys, os
sys.path.append("\\".join([os.path.dirname(os.path.abspath(__file__)), "RepScraper"]))
from .models import Post, Review
from forms import FilterForm

class Filter:
    def __init__(self):
        self.reviews = Review.objects.all()

    def process(self, args):
        for a in args:
            self.reviews = self.filter(a, args[a])

    def filter(self, attr, key):
        filtered_reviews = []

        for review in self.reviews:
            if key in getattr(review, attr):
                filtered_reviews.append(review)

        return filtered_reviews

        
            

class AppView(TemplateView):
    template_name = 'webapp/home.html'

    def get(self, request):
        #posts = scraper.scrape_reddit()
        print('GET Request Recieved')

        form = FilterForm()

        return render(request, self.template_name, {"filter": form, "reviews": Review.objects.all()})

    def post(self, request):
        form = FilterForm(request.POST)

        args = {}

        if form.is_valid():
            if form.cleaned_data['user'].strip() !=  '':
                print('User is Added')
                args['user'] = form.cleaned_data['user']
            if form.cleaned_data['itemName'].strip() != '':
                print('Item Name is Added')
                args['itemName'] = form.cleaned_data['itemName']

        f = Filter()
        f.process(args)

        return render(request, self.template_name, {"filter": form, "reviews": f.reviews})