import csv
import random
import warnings
import os

from locust import HttpUser, task, between

SEARCH_LINK = "/search_reserved_keyword?q=covidessentialproduct&aggregated=1"


class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', 'https://search.sastasundar.com')
    wait_time = between(1, 5)

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False
    @task
    def sasta_sundar_search_query(self):
        self.client.get(SEARCH_LINK)
