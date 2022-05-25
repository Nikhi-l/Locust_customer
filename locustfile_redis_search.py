import warnings
import os

from locust import HttpUser, task, between

SEARCH_LINK = ""


class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', 'https://search.sastasundar.com/search_reserved_keyword?q=best-deal&aggregated=1&token=&device=5&wh=1&panindia=0&pincode=700102&exclude_items=1&page=2&size=1')
    wait_time = between(1, 5)

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.get(SEARCH_LINK)
