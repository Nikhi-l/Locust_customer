import csv
import random
import warnings
import os

from locust import HttpUser, task, between

SEARCH_LINK = "/search?q={param}"
device_id = "f21e21e1-a1bd-4b9e-a620-6da754085a9e"


body_cart_checkout = {"products": [{"product_id": "9841", "quantity": 1, "ref_id": ""}]}
smallcase_char = "abcdefghijklmnopqrstuvwxyz"





class SastaSundarSearch(HttpUser):
    host = os.getenv('TARGET_URL', '')
    SEARCH_QUERIES = []

    def get_mobile_number(self):
        no = ""
        for i in range(0, 10):
            x = random.randint(5, 9)
            no = no + str(x)
        return no

    def get_device_id(self):
        id = ""
        for ch in device_id:
            if 'a' <= ch <= 'z':
                id = id + random.choice(smallcase_char)
            elif '1' <= ch <= '9':
                id = id + str(random.randint(1, 9))
            else:
                id = id + ch;
        # print(id)
        return id;
    def init(self):
        self.body_get_otp = {
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

        self.body_verify_otp = {
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

        self.header_cart_checkout = {
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


    def on_start(self):
        warnings.filterwarnings("ignore")
        self.client.verify = False
        self.init()
        # self.fetch_search_queries()
        self.body_get_otp["Params"]["MobileNo"] = self.get_mobile_number()
        self.body_get_otp["RequestHeader"]["DeviceId"] = self.get_device_id()
        self.body_verify_otp["Params"]["MobileNo"] = self.body_get_otp["Params"]["MobileNo"]
        self.body_verify_otp["RequestHeader"]["DeviceId"] = self.body_get_otp["RequestHeader"]["DeviceId"]
        self.header_cart_checkout["deviceid"] = self.body_get_otp["RequestHeader"]["DeviceId"]
        self.login()

    def login(self):
        response = self.client.post(
            "https://fkhp-preprod-api.sastasundar.com/sastasundar/customer/rest_customer/postData",
            json=self.body_get_otp)
        print(response.text)
        if response.status_code == 200:
            # print(response.text)
            json_response = response.json()
            self.body_verify_otp["Params"]["OTP"] = json_response["ResponseData"]["data"]
            response = self.client.post(
                "https://fkhp-preprod-api.sastasundar.com/sastasundar/customer/rest_customer/postData",
                json=self.body_verify_otp
            )
            print(response.text)
            json_response = response.json()
            if json_response["ResponseData"].get("data", {}) != {}:
                print(response.text)
                self.header_cart_checkout["userid"] = str(json_response["ResponseData"]["data"]["UserId"])
            print("Logged In")

    @task
    def sasta_sundar_search_query(self):
        response = self.client.post("https://preprod-fkhapi.sastasundar.com/checkout",
                                    headers=self.header_cart_checkout,
                                    json=body_cart_checkout)
        # print(response.text)
