import csv
import random
import warnings
import os

from locust import HttpUser, task, between

SEARCH_LINK = "/?name={param}"

class SastaSundarCheckout(HttpUser):
    host = os.getenv('TARGET_URL', 'https://api.agify.io')
    SEARCH_QUERIES = []

    def fetch_search_queries(self):
        files = [open("found + retail-customer + all-devices + all-scope + (2022-02-01 to 2022-02-08).csv"),
                 open("not-found + retail-customer + all-devices + all-scope + (2022-02-01 to 2022-02-08).csv")]
        for file in files:
            csv_reader = csv.reader(file)
            for name in csv_reader:
                self.SEARCH_QUERIES.append(name)

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False
        self.fetch_search_queries()

    @task
    def sasta_sundar_search_query(self):
        self.client.get(SEARCH_LINK.format(param=random.choice(self.SEARCH_QUERIES)))