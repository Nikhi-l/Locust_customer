
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
    "Section": "getCouponList"
  },
  "Params": {
    "products": [],
    "UserId": "NDkzNzcyNA==",
    "Pincode": "700156",
    "PanIndia": "0",
    "HideCouponList": "0",
    "warehouseId": "1"
  }
}
class SastaSundarAddToCart(HttpUser):
    host = os.getenv('TARGET_URL', 'https://api.sastasundar.com')

    def on_start(self):
        self.client.verify = False
        warnings.filterwarnings("ignore")

    @task
    def sasta_sundar_get_coupons(self):
        response = self.client.post("/sastasundar/index.php/cart/rest_cart/postData", data = body, auth=None)