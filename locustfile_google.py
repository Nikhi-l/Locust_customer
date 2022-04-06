import csv
import random
import warnings
import os

from locust import HttpUser, task, between


class SastaSundarCheckout(HttpUser):
    host = os.getenv('TARGET_URL', 'http://www.7timer.info')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get("/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=json")