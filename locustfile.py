import csv
import random
import warnings
import os

from locust import HttpUser, task, between

# SEARCH_LINK = "/product_list_v2/?q={param}&ptype=P&mtype=1&panindia=0&pincode=226002&format=2&wh=2&salt_code=&token" \
#               "=7il9iil94il9oil97il9o7l&include_discontinued=1&strict_match=1&includeGiftable=1&fallback=0" \
#               "&csrf_test_name=f4cfa96ab9aee18162f46900e4694df6&_=1645763513346 "

SEARCH_LINK = "/search?q={param}"
SEARCH_QUERIES = []


# for multiple users sending different queries

class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', 'https://stage-search.sastasundar.com')
    wait_time = between(1, 5)
    def fetch_search_queries(self):
        files = [open("found + retail-customer + all-devices + all-scope + (2022-02-01 to 2022-02-08).csv"),
                 open("not-found + retail-customer + all-devices + all-scope + (2022-02-01 to 2022-02-08).csv")]
        for file in files:
            csv_reader = csv.reader(file)
            for name in csv_reader:
                SEARCH_QUERIES.append(name)

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False
        self.fetch_search_queries()

    @task
    def sasta_sundar_search_query(self):
        self.client.get(SEARCH_LINK.format(param=random.choice(SEARCH_QUERIES)))
        # print(response.status_code)
