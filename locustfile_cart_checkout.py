import csv
import random
import warnings
import os

from locust import HttpUser, task, between

SEARCH_LINK = "/search?q={param}"

body_get_otp = {
    "RequestHeader": {
        "AppType": "N",
        "AppVersion": "4.0.4",
        "AppVersionCode": "109",
        "DeviceId": "f21e21e1-a1bd-4b9e-a620-6da754085a9e",
        "DeviceDensity": "440",
        "DeviceDensityType": "xhdpi",
        "DeviceHeight": "2160",
        "DeviceWidth": "1080",
        "DeviceName": "Google Pixel 4a",
        "DeviceOsInfo": "12",
        "NetworkInfo": "Wifi",
        "AccessToken": "PDWZ5pStjE"
    },
    "RequestURI": {
        "Section": "regenerateOtp"
    },
    "Params": {
        "MobileNo": "9051026063",
        "UserIP": "",
        "UserAgent": "Dalvik/2.1.0 (Linux; U; Android 12; Pixel 4a Build/SQ1A.220205.002)",
        "CampaignId": "",
        "warehouseId": "",
        "PanIndia": "0",
        "Latitude": "",
        "Longitude": "",
        "Pincode": ""
    }
}

body_verify_otp = {
    "RequestHeader": {
        "AppType": "N",
        "AppVersion": "4.0.4",
        "AppVersionCode": "109",
        "DeviceId": "f21e21e1-a1bd-4b9e-a620-6da754085a9e",
        "DeviceDensity": "440",
        "DeviceDensityType": "xhdpi",
        "DeviceHeight": "2160",
        "DeviceWidth": "1080",
        "DeviceName": "Google Pixel 4a",
        "DeviceOsInfo": "12",
        "NetworkInfo": "Wifi",
        "AccessToken": "PDWZ5pStjE"
    },
    "RequestURI": {
        "Section": "verifyOtp"
    },
    "Params": {
        "MobileNo": "9051026063",
        "OTP": "32529",
        "UserIP": "",
        "UserAgent": "Dalvik/2.1.0 (Linux; U; Android 12; Pixel 4a Build/SQ1A.220205.002)",
        "CampaignId": "",
        "IsLocationRequired": "Y",
        "LocationData": {
            "Pincode": "",
            "StateId": "",
            "StateName": "",
            "StateCode": "",
            "CityId": "",
            "CityName": "",
            "LocationSkipped": ""
        }
    }
}

header_cart_checkout = {
    "Content-Type": "application/json",
    "apptype": "N",
    "appversion": "4.0.5",
    "appversioncode": "109",
    "deviceid": "f21e21e1-a1bd-4b9e-a620-6da754085a9e",
    "userid": "5108874",
    "pincode": "700156",
    "is_panindia": "0",
    "warehouse_id": "1"
}

body_cart_checkout = {"products": [{"product_id": "9841", "quantity": 1, "ref_id": ""}]}

def get_mobile_number():
    no = ""
    for i in range(0, 10):
        x = random.randint(0,9)
        no = no + str(x)
    return no


class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', '')
    wait_time = between(1, 5)
    SEARCH_QUERIES = []

    def fetch_search_queries(self):
        files = [open("found + retail-customer + all-devices + all-scope + (2022-02-01 to 2022-02-08).csv"),
                 open("not-found + retail-customer + all-devices + all-scope + (2022-02-01 to 2022-02-08).csv")]
        for file in files:
            csv_reader = csv.reader(file)
            for name in csv_reader:
                self.SEARCH_QUERIES.append(name)

    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False
        # self.fetch_search_queries()
        self.login()

    def login(self):
        body_get_otp["Params"]["MobileNo"] = get_mobile_number()
        body_verify_otp["Params"]["MobileNo"] = body_get_otp["Params"]["MobileNo"]
        response = self.client.post(
            "https://fkhp-preprod-api.sastasundar.com/sastasundar/customer/rest_customer/postData", json=body_get_otp)
        if response.status_code == 200:
            print(response.text)
            json_response = response.json()
            body_verify_otp["Params"]["OTP"] = json_response["ResponseData"]["data"]
            response = self.client.post(
                "https://fkhp-preprod-api.sastasundar.com/sastasundar/customer/rest_customer/postData",
                json=body_verify_otp
            )
            json_response = response.json()
            if json_response["ResponseData"].get("data", {}) != {}:
                print(response.text)
                header_cart_checkout["userid"] = str(json_response["ResponseData"]["data"]["UserId"])
                header_cart_checkout["deviceid"] = json_response["AppHeader"]["DeviceId"]
                # print("Logged In")

    @task
    def sasta_sundar_search_query(self):
        response = self.client.post("https://preprod-fkhapi.sastasundar.com/checkout", headers=header_cart_checkout,
                                    json=body_cart_checkout)
        # print(response.text)
