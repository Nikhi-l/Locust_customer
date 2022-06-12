import warnings
import os
import random
from locust import HttpUser, task, between
import uuid

body = {
    "MobileNo": "9999559994",
    "EmailId": "abc@abc.com",
    "FirstName": "first",
    "LastName": "last",
    "identityToken": "qwer322"
}


class SastaSundarAddToCart(HttpUser):
    host = os.getenv('TARGET_URL', 'https://fkhp-preprod-fe.sastasundar.com')

    def get_mobile_number(self):
        no = ""
        for i in range(0, 10):
            x = random.randint(1, 9)
            no = no + str(x)
        return no

    def get_token(self):
        return uuid.uuid1()

    def on_start(self):
        self.client.verify = False
        warnings.filterwarnings("ignore")

    @task
    def sasta_sundar_get_coupons(self):
        body["MobileNo"] = self.get_mobile_number()
        body["identityToken"] = self.get_token()
        with self.client.post("/index.php/webapi/fkh_app_in_app/AutoLogin_LoadTesting", catch_response=True,
                              data=body) as response:
            print(response.text)
            try:
                json_response = response.json()
                if response.status_code == 200:
                    if json_response.get("data", {}).get("data", {}).get("UserId", "null") != "null":
                        response.success()
                    else:
                        response.failure(f'UserId not received in response!')
                else:
                    response.failure(f'status code {response.status_code}')
            except:
                pass
