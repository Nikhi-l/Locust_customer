import csv
import random
import warnings
import os

from locust import HttpUser, task, between

SEARCH_LINK = "/home/gettopbanner"

body = {"warehouseId": "1", "profileId": "1", "panindia": "0"}


class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', 'https://catalog.sastasundar.com')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.post(SEARCH_LINK, data=body)
