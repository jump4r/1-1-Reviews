from django.apps import AppConfig
import os
import subprocess

class WebappConfig(AppConfig):
    name = 'webapp'
    verbose_name = "1:1 Rep Aggregator"
    def ready(self):
        print('Starting Streamer (From WebappConfig)')
        scraper_path = '\\'.join([os.path.dirname(os.path.abspath(__file__)), 'RepScraper', 'scraper.py'])

        #print(check_to_run.checkint)
        #subprocess.Popen(['python', scraper_path]) 
        