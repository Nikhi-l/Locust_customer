import csv
import random
import warnings
import os

from locust import HttpUser, task, between, TaskSet


class SastaSundarSearch(TaskSet):
    host = os.getenv('TARGET_URL', 'https://www.google.com')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task(1)
    def a(self):
        self.client.get("/search?q=a")

    @task(2)
    def b(self):
        self.client.get("/search?q=b")

    @task(5)
    def b(self):
        self.client.get("/search?q=c")

    @task(15)
    def b(self):
        self.client.get("/search?q=d")

    @task(100)
    def b(self):
        self.client.get("/search?q=e")