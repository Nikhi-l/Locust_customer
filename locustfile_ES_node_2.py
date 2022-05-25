import csv
import random
import warnings
import os

from locust import HttpUser, task, between


SEARCH_LINK = "/search_list/?q={keyword}&panindia={panindia}&wh={wh}&mtype=1&include_discontinued=1&strict_match=1&includeGiftable=1&csrf_test_name=&env=d"

class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', 'https://search.sastasundar.com')
    wait_time = between(1, 5)
    KEYWORDS = []
    WH = [1,2,3,4,5,6,7,8]
    PAN_INDIA = [0, 1]

    def fetch_search_queries(self):
        file = open("keywords.csv")
        csv_reader = csv.reader(file)
        for name in csv_reader:
            self.KEYWORDS.append(name)

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False
        self.fetch_search_queries()

    @task
    def sasta_sundar_search_query(self):
        self.client.get(SEARCH_LINK.format(keyword=random.choice(self.KEYWORDS),
                                            wh=random.choice(self.WH),
                                         panindia=random.choice(self.PAN_INDIA)))
