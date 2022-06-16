import csv
import random
import warnings
import os

from locust import HttpUser, task, between


class SastaSundarCheckout(HttpUser):
    link = "/category/getL3categoryProductList/?cat_id={param}&panindia=0&warehouseId=1&pincode=700156"
    host = os.getenv('TARGET_URL', 'https://catalog.sastasundar.com')
    ids = ["fhblrz", "hjkn36"]

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get(self.link.format(param=random.choice(self.ids)))
