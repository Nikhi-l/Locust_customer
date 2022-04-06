import csv
import random
import warnings
import os

from locust import HttpUser, task, between


class SastaSundarCheckout(HttpUser):
    host = os.getenv('TARGET_URL', 'http://sample-go-service-dev.ap-south-1.elasticbeanstalk.com')


    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get("/")