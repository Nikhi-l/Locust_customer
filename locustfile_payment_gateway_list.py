import warnings
import os

from locust import HttpUser, between, task


class SastaSundarAddToCart(HttpUser):
    host = os.getenv('TARGET_URL', 'https://fkhapi.sastasundar.com')


    def on_start(self):
        self.client.verify = False
        warnings.filterwarnings("ignore")


    @task
    def sasta_sundar_search_query(self):
        self.client.request(method="GET", url="/payment/pglist?mobile_number=6290708028", auth=None, headers={
                                    "Apptype": "N",
                                    "Deviceid": "81653dce-0dd2-4201-8916-4aecbdd89269",
                                    "Userid": "4937724"})
        self.client.cookies.clear()