from flask import Flask, json, request, redirect, url_for, Response, jsonify
import jwt
from backend.food_bank_api import Food_Bank
from backend.expiry import Expiry_date
from backend.Google_cloud import Google
import re
import random
from threading import Timer
from backend.Google_places import Places
from pyfcm import FCMNotification

app = Flask(__name__)
SECRET = 'mysecret'
UPLOAD_FOLDER = './data/'
userLocation = ()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
REGISTERED_DEVICE_ID = None
FOOD_PR = None
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
        if "device_id" in req_object:
            global REGISTERED_DEVICE_ID
            REGISTERED_DEVICE_ID = req_object['token']
        if "loc" in req_object:
            global userLocation
            userLocation = req_object['loc'].split(",")
        #     print("userLocation: ", tuple(userLocation))
        # print("request: ", req_object)
        encoded = jwt.encode(req_object, SECRET, algorithm='HS256')
        # print("encoded: ", encoded)
        return jsonify({"token": str(encoded, 'utf-8')}), 200
    else:
        return jsonify({"status": "Failed",
                        "reason": "Not a json"}), 400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/permission', methods=['POST'])
def firebase_auth():
    if request.is_json:
        req_object = request.get_json()
        global REGISTERED_DEVICE_ID
        REGISTERED_DEVICE_ID = req_object["registration_id"]
        return jsonify({"api_key"})


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    # print('request', request.files)
    if 'bill' not in request.files:
        return jsonify({"status": "Failed",
                        "reason": "bill is not in request.files"}), 400
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

        a, b = caller(file)
        return jsonify(a)
        # return jsonify([{
        #     "days": 1,
        #     "product": "fresh"
        # },
        #     {
        #         "days": 3,
        #         "product": "Onions"
        #     },
        #     {
        #         "days": 3,
        #         "product": "pound"
        #     },
        #     {
        #         "days": 14,
        #         "product": "Radishes"
        #     }])
    else:
        return jsonify({"status": "Failed",
                        "reason": "File name not valid"}), 400


@app.route('/donate', methods=['GET'])
def donate():
    p = Places()
    loc_dict = []
    organization, place_id, location = p.get_nearby_worship()
    print(organization)
    for i in range(min(3,len(organization))):
        loc_dict.append({})
        loc_dict[i]['organization'] = organization[i]
        loc_dict[i]['lat'] = location[i][0]
        loc_dict[i]['long'] = location[i][1]
    return jsonify(loc_dict)


def caller(image):
    ocr_obj = Google()
    ocr_text = ocr_obj.get_text()
    fd = Food_Bank()
    exp = Expiry_date()
    food_dict = []
    index = 0
    cost_dict = {}
    food_item = None
    for line in ocr_text:
        if "$" in line and food_item != None and isinstance(food_item, str):
            p = re.compile(r"\d+\.*\d*")
            if len(p.findall(line)) > 0:
                cost_dict[food_item] = p.findall(line)[0]
            else:
                cost_dict[food_item] = "$1.50"
        else:
            food_item = fd.get_food(line)
            if food_item:
                if " " in food_item:
                    food_item = food_item.split(" ")
                    for food in food_item:
                        food = food.strip(',')
                        expiry_days = exp.get_expiry_date(food)
                        if expiry_days:
                            food_dict.append({})
                            food_dict[index]['product'] = food
                            food_dict[index]['days'] = expiry_days
                            # food_dict[index]['cost']=cost_dict[food_item]
                            index += 1
                            food_item = food
                            break
                else:
                    expiry_days = exp.get_expiry_date(food_item)
                    if expiry_days:
                        food_dict[index]['product'] = food_item
                        food_dict[index]['days'] = expiry_days
                        # food_dict[index]['cost']=cost_dict[food_item]
                        index += 1
    ingred = []
    for i in range(0, min(3, len(food_dict))):
        ingred.append(food_dict[i]['product'])
    FOOD_PR = food_dict
    run_scheduled_task(ingred, FOOD_PR)
    return json.dumps(food_dict), json.dumps(cost_dict)


@app.route('/organizations', methods=['GET'])
def get_organizations():
    p = Places()
    loc_dict = {}
    organization, place_id, location = p.get_nearby_worship()
    # print("organization, place_id, location:", organization, place_id, location)
    for i in range(len(organization)):
        loc_dict[organization[i]] = {  # 'place_id': place_id[i],
            'location': {'lat': location[i][0], 'long': location[i][1]}}

    return jsonify(loc_dict)


def send_recipe(ingredients):
    fd = Food_Bank()
    return fd.get_recipe(ingredients)


def run_scheduled_task(ingredients, FOOD_PR):
    ingr = ''
    # print("Ingr: ", ingredients)
    for item in ingredients:
        ingr += item + ","
    timer = Timer(2, send_notification, [ingr], {'f': FOOD_PR})
    timer.start()


def send_notification(*farg, **kwargs):
    # print(farg)
    ingredients = farg[0]
    food = kwargs['f']

    recipes = send_recipe(ingredients)
    print("8******************************\nrecipes:", recipes)
    push_service = FCMNotification(
        api_key="AAAAeyivA7M:APA91bHUVruxK72d9e-TQ_tWEj7MRUfYrLUjlAydZz0hwTT8yJ6xLVy4KEFhRdeLrqlkwP97u99raBXIps5UxMcDwxlRcVTxziT0PTFI8ExzR1SEa6clMKkFuT2X56nd4kY7or7J5hkM")

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
    notify_about = {}
    notify_about['expires'] = []
    index = 0

    # for food in food:
    #     if food['days'] <= 3:
    #         notify_about['expires'].append(food['product'])
    # notify_about['recipes'] = recipes
    # message_body = notify_about

    message_title = "Food Expiration Alert"

    message_body = "Hi, we noticed that " + ", ".join(list(map(lambda x: x["product"], food))[
                                                      :3]) + " are expiring and you should consume them by Thursday. Alternatively, you could use them to make " + ", ".join(
        list(map(lambda x: x["recipe"], recipes))[:3])
    print("message_body: ", message_body)
    # message_body = "notify_about"
    # global REGISTERED_DEVICE_ID
    #     # print("REGISTERED_DEVICE_ID: ", REGISTERED_DEVICE_ID)

    result = push_service.notify_single_device(
        registration_id="fivC8EoC9w4:APA91bFA7ms8lrPsWpW5OXLtLIfGcMNmUcM7MM2pb4j7iZhN8m5ZSBbImnnkUjlW5yON3UHaXgLcMiX1N3lmapsPWhyDPDQcKOwcJsH-PzMI91tMgY7j72P14ZmLny0Ze9_oihAPqtir",
        data_message={"url": "http://google.com"},
        message_title=message_title,
        message_body=json.dumps(message_body))
    # print(result)
    # print(notify_about)


def get_fact():
    with open("../food_db/Food_wastage_facts.txt", 'r') as f:
        lines = f.read()
        lines = lines.split("\n")
    return (lines[random.randint(0, len(lines) - 1)])


'''
def final_json():
    final_dict={}
    final_dict['food']=
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
