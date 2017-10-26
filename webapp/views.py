from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sys, os
from pprint import pprint
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
            if key.lower() in getattr(review, attr).lower():
                print(key + ' found in ' + getattr(review, attr))
                filtered_reviews.append(review)

        return filtered_reviews

    def filter_by_id(self, id_string, reviews):
        ids = id_string.split(',')

        filtered_reviews = []

        for review in reviews:
            if (str(review.id) in ids):
                # print('Found Review ' + str(review.id) + ' in ' + str(ids))
                filtered_reviews.append(review)

        self.reviews = filtered_reviews

class Query:
    def __init__(self, user='', item=''):
        self.args = { 'user': user, 'itemName': item }

class AppView(TemplateView):
    template_name = 'webapp/home.html'

    def get(self, request):
        
        args = { }

        args['user'] = request.GET.get('user') if (request.GET.get('user') != None) else ''   
        args['itemName'] = request.GET.get('item') if (request.GET.get('item') != None) else ''

        is_filtered = True if (args['user'] != '' or args['itemName'] != '') else False

        query_string = '?'  
        if (is_filtered):
            query_string += ('user=' + args['user'] + '&') if (args['user'] != '') else ''
            query_string += ('item=' + args['itemName'] + '&') if (args['itemName'] != '') else ''
        
        bookmarks_only = True if (request.GET.get('ids') != None) else False
        query_string += ('ids=' + request.GET.get('ids') + '&') if bookmarks_only else ''

        f = Filter()
        f.process(args)

        if bookmarks_only:
            f.filter_by_id(request.GET.get('ids'), f.reviews)

        paginator = Paginator(f.reviews, 10)
        page = request.GET.get('page')

        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {"request": request.GET, "reviews": reviews, "is_filtered": is_filtered, "query": query_string, "bookmarks_only": bookmarks_only })