import csv
import random
import warnings
import os

from locust import HttpUser, task, between


class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', '')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get("/")
