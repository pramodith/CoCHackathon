import urllib
import requests
import json
from flask import jsonify
import pprint
class Google:

    def __init__(self,bucket_location="gs://verve2/bill1.jpeg"):
        self.api_id=""
        self.api_key="AIzaSyDaDPJZIvneH9hGsvC_EjR7UyE-0VP1Ud0"
        self.url="https://vision.googleapis.com/v1/images:annotate?key="+self.api_key
        self.bucket_location=bucket_location

    def get_text(self):
        data = {"requests": [{
            "image": {
                "source": {"imageUri": self.bucket_location}
            },
            "features": [
                {
                    "type": "TEXT_DETECTION"
                }
            ]

        }]
        }
        print(json.dumps(data))
        response=requests.post(self.url,headers = {'Content-Type': "application/json", 'Accept': "application/json"},json=data)
        pp = pprint.PrettyPrinter(width=3, compact=True)
        food = (response.json())

        food_items=food['responses'][0]['textAnnotations'][0]['description']
        food_items=food_items.split("\n")
        return food_items


