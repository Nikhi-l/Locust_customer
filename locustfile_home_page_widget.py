import csv
import random
import warnings
import os

from locust import FastHttpUser, task, between

body = {
  "page":1,
  "panindia":0,
  "warehouseId":"1",
  "pincode":700120,
  "userId":"4937724",
  "profileId":"",
  "app_type":"N",
  "app_version":"4.0.4",
  "app_version_code":109,
  "resolution_type":"xhdpi",
  "deviceId":"81653dce-0dd2-4201-8916-4aecbdd89269",
  "IsLab":1
}

header = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "198",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "okhttp/5.0.0-alpha.2"
}

class SastaSundarCheckout(FastHttpUser):
    host = os.getenv('TARGET_URL', 'https://catalog.sastasundar.com')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        self.client.post("/home/getmasterhomewidgets", headers=header, data=body)
        self.client.cookies.clear()