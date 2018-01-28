# import os
from flask import Flask, json, request, redirect, url_for, Response, jsonify
import jwt
from backend.food_bank_api import Food_Bank
from backend.expiry import Expiry_date
from backend.Google_cloud import Google
import pyfcm
import re
from threading import Timer
from backend.Google_places import places
# from werkzeug.utils import secure_filename

#import firebase_admin
#from firebase_admin import credentials

from oauth2client.service_account import ServiceAccountCredentials

#cred = credentials.Certificate("../auth/Chiroptera-b1c2c21ccfd4.json")
#firebase_admin.initialize_app(cred)


app = Flask(__name__)
SECRET = 'mysecret'
UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
REGISTERED_DEVICE_ID=None

'''
def _get_access_token():
    """
    Retrieve a valid access token that can be used to authorize requests.
    :return: Access token.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name("../auth/Chiroptera-b1c2c21ccfd4.json", "https://www.googleapis.com/auth/firebase.messaging")
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token
'''

'''
@app.route("/gctoken")
def get_access_token():
    return jsonify({"token": _get_access_token()}), 200
'''

@app.route("/ping")
def ping():
    return "pong"


@app.route("/login", methods=['POST'])
def login():
    if request.is_json:
        req_object = request.get_json()
        print("request: ", req_object)
        encoded = jwt.encode(req_object, SECRET, algorithm='HS256')
        print("encoded: ", encoded)
        return jsonify({"token": str(encoded,'utf-8')}), 200
    else:
        return jsonify({"status": "Failed",
                        "reason": "Not a json"}), 400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/permission',methods=['POST'])
def firebase_auth():
    if request.is_json:
        req_object = request.get_json()
        REGISTERED_DEVICE_ID=req_object["regiatration_id"]
        return jsonify({"api_key"})

@app.route('/test',methods=['GET'])
def send_notification():
    from pyfcm import FCMNotification

    push_service = FCMNotification(api_key="AAAAkn0q-qU:APA91bG4dp-bdQfYD3zSJwZnFYiWXnYMLI6BtNDl-yJSQW2hnSW1dwH_Yw1qTayryoDXPVZeOsUw9ZoQKXRDiHINnIw4u4oSchiaE3wPWFIVqcAkMpkfPH5eneZZRjKdnltTcn1PUafu")

    # OR initialize with proxies
    '''
    proxy_dict = {
        "http": "http://127.0.0.1",
        "https": "http://127.0.0.1",
    }
    push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)
    '''
    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = "<device registration_id>"
    message_title = "Uber update"
    message_body = "Hi john, your customized news for today is ready"
    result = push_service.notify_single_device(registration_id="asbdaf", message_title=message_title,
                                               message_body=message_body,)

    print(result)

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    print('request', request.files)
    if 'bill' not in request.files:
        return jsonify({"status": "Failed",
                        "reason": "bill is not in request.files" }), 400
    file = request.files['bill']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return jsonify({"status": "Failed",
                        "reason": "No selected file"}), 400
    if file and allowed_file(file.filename):
        # call OCR method here

        # filename = secure_filename(file.filename)
        # file.save(os.path.join(UPLOAD_FOLDER, filename))
        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
        return jsonify([{"milk": "5d"}, {"bread": "2d"}, {"eggs": "7d"}])
    else:
        return jsonify({"status": "Failed",
                        "reason": "File name not valid"}), 400

def caller(image):
    ocr_obj=Google()
    ocr_text=ocr_obj.get_text()
    fd=Food_Bank()
    exp=Expiry_date()
    food_dict={}
    cost_dict={}
    food_item=None
    for line in ocr_text:
        if "$" in line and food_item!=None:
            p = re.compile(r"\d+\.*\d*")
            if len(p.findall(line))>0:
                cost_dict[food_item] = p.findall(line)[0]
            else:
                cost_dict[food_item]="$1.50"
        else:
            food_item = fd.get_food(line)
            food_item=food_item.split(" ")
            for food in food_item:
                food=food.strip(',')
                expiry_days = exp.get_expiry_date(food)
                if expiry_days:
                    food_dict[food_item]=expiry_days
                    break

    return json.dumps(food_dict),json.dumps(cost_dict)

def get_organiztion():
    p=places()
    loc_dict={}
    organization,place_id,location=p.get_nearby_charities()
    for i in range(len(organization)):
        loc_dict[organization[i]]={'place_id':place_id[i],'location':{'lat':location[i]['lat'],'long':location[i]['long']}}
    return jsonify(loc_dict)

def send_recipe(ingredients):
    fd=Food_Bank()
    return fd.get_recipe(ingredients)

def run_scheduled_task():
    timer = Timer(10, send_notification)
    timer.start()

'''
def final_json():
    final_dict={}
    final_dict['food']=
'''

if __name__ == '__main__':
   app.run(host='0.0.0.0')