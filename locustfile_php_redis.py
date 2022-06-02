import csv
import random
import warnings
import os

from locust import HttpUser, task, between


SEARCH_LINK = "/nfr_redis?key={param}"




class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', 'https://healthplus.flipkart.com')
    wait_time = between(1, 5)
    SEARCH_QUERIES = []

    def fetch_search_queries(self):
        for i in range(1, 51):
            self.SEARCH_QUERIES.append(str("nfr_" + str(i)))

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False
        self.fetch_search_queries()

    @task
    def sasta_sundar_search_query(self):
        self.client.get(SEARCH_LINK.format(param=random.choice(self.SEARCH_QUERIES)))
