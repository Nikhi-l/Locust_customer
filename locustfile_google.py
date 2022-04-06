import csv
import random
import warnings
import os

from locust import HttpUser, task, between


class SastaSundarCheckout(HttpUser):
    host = os.getenv('TARGET_URL', 'https://newsapi.org')


    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get("/v2/top-headlines?country=us&category=business&apiKey=eb87d9b1b57d4c25a6fa5049d2014794")