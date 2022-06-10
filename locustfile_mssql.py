import csv
import random
import warnings
import os

from locust import HttpUser, task, between

SEARCH_LINKS = "/index.php/chk_dtbs/m1"


class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', 'https://fkhp-preprod-fe.sastasundar.com')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get(SEARCH_LINKS)
