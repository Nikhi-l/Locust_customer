import csv
import random
import warnings
import os

from locust import HttpUser, task, between


class SastaSundarCheckout(HttpUser):
    host = os.getenv('TARGET_URL', 'http://11.17.20.85')


    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get("/index.php/orders/order/lastOrders?CustUserId=418637")
