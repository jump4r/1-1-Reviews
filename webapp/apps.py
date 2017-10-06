from django.apps import AppConfig
import os
import subprocess

class WebappConfig(AppConfig):
    name = 'webapp'
    verbose_name = "1:1 Rep Aggregator"
    def ready(self):
        print('Starting Streamer (From WebappConfig)')
        streamer_path = '\\'.join([os.path.dirname(os.path.abspath(__file__)), 'RepScraper', 'streamer.py'])

        subprocess.Popen(['python', streamer_path]) 