from django.apps import AppConfig
import os, sys
import subprocess

class WebappConfig(AppConfig):
    name = 'webapp'
    verbose_name = "1:1 Rep Aggregator"
    def ready(self):
        print('Starting Streamer (From WebappConfig)')
        
        scraper_path = '\\'.join([os.path.dirname(os.path.abspath(__file__)), 'RepScraper', 'scraper.py'])
        sys.path.append('\\'.join([os.path.dirname(os.path.abspath(__file__)), 'RepScraper']))
        from streamer import Streamer

        s = Streamer()
        #s.stream()
        