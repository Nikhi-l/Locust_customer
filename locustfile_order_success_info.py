import csv
import random
import warnings
import os

from locust import HttpUser, task, between

body = {
    "orderids":"8933318847"
}

header = {
    "Host": "fkhapi.sastasundar.com",
    "Apptype": "N",
    "Appversion": "4.0.4",
    "Appversioncode": "109",
    "Deviceid": "81653dce-0dd2-4201-8916-4aecbdd89269",
    "Devicedensity": "320",
    "Devicedensitytype": "xhdpi",
    "Deviceheight": "1184",
    "Devicewidth": "768",
    "Devicename": "Unknown Google Nexus 4",
    "Deviceosinfo": "5.1",
    "Networkinfo": "Wifi",
    "Accesstoken": "PDWZ5pStjE",
    "Refdeviceid": "4dd29c0f2f8d1842",
    "Userid": "4937724",
    "Pincode": "700120",
    "Is_panindia": "0",
    "Warehouse_id": "1",
    "Content-Type": "application/json",
    "Content-Length": "25",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "okhttp/5.0.0-alpha.2"

}

class SastaSundarCheckout(HttpUser):
    host = os.getenv('TARGET_URL', 'https://fkhapi.sastasundar.com')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        response = self.client.post("/orderinfo/ordersuccessinfo", headers=header, json=body)