import csv
import random
import warnings
import os

from locust import HttpUser, task, between

SEARCH_LINKS = ["/search_list?q=dettol&env=d", "/search_list?q=honey&env=d", "/search_list?q=dabur&env=d",
                "/search_list?q=dettol+handwash&env=d"]


class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', 'https://search.sastasundar.com')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get(random.choice(SEARCH_LINKS))
