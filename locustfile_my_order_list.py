import csv
import random
import warnings
import os

from locust import HttpUser, task, between

body = {
  "RequestHeader": {
    "AppType": "N",
    "AppVersion": "4.0.4",
    "AppVersionCode": "109",
    "DeviceId": "81653dce-0dd2-4201-8916-4aecbdd89269",
    "DeviceDensity": "320",
    "DeviceDensityType": "xhdpi",
    "DeviceHeight": "1184",
    "DeviceWidth": "768",
    "DeviceName": "Unknown Google Nexus 4",
    "DeviceOsInfo": "5.1",
    "NetworkInfo": "Wifi",
    "AccessToken": "PDWZ5pStjE"
  },
  "RequestURI": {
    "Section": "myOrderList"
  },
  "Params": {
    "UserId": "NDkzNzcyNA==",
    "RecordPerPage": "15",
    "ItemCount": "2",
    "PageNo": "1"
  }
}

header = {
    "Host": "api.sastasundar.com",
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": "450",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "okhttp/5.0.0-alpha.2"

}

class SastaSundarCheckout(HttpUser):
    host = os.getenv('TARGET_URL', 'https://api.sastasundar.com')

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False

    @task
    def sasta_sundar_search_query(self):
        response = self.client.post("/sastasundar/index.php/order/rest_order/postData", headers=header, json=body)