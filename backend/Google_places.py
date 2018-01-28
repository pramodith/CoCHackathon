import requests
import urllib
import json


class places:

    def __init__(self,home_lat=33.775618,home_long=-84.396285):
        self.lat=home_lat
        self.long=home_long
        #self.work_lat=work_lat
        #self.work_long=work_long
        self.api_key="AIzaSyDaDPJZIvneH9hGsvC_EjR7UyE-0VP1Ud0"
        self.radius=10000
        self.url_nearby="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
        self.url_textsearch="https://maps.googleapis.com/maps/api/place/textsearch/json?query="
        self.url_directions="https://https://maps.googleapis.com/maps/api/directions/json?origin"
        self.possible_type=['church','hindu_temple','synagogue','mosque']
        self.place_ids=[]
        self.location=[]
    def get_nearby_worship(self):
        organizations=[]
        for type in self.possible_type:
            response=requests.get(self.url_nearby+str(self.lat)+","+str(self.long)+"&radius="+str(self.radius)+"&type="+type+"&key="+self.api_key)
            places=response.json()
            for result in places['results']:
                self.location.append((result['geometry']['location']['lat'],result['geometry']['location']['lng']))
                self.place_ids.append(result['place_id'])
                organizations.append(result['name'])
        return organizations,self.place_ids,self.location

    def get_nearby_charities(self):
        query=urllib.parse.quote_plus("charities near me")
        organizations = []
        response = requests.get(self.url_textsearch +query+ str(self.lat) + "," + str(self.long) + "&radius=" + str(
                self.radius) + "&key=" + self.api_key)
        print(response.content)
        places = response.json()
        print(places)
        for result in places['results']:
            organizations.append(result['name']+": "+result['formatted_address'])

    def get_directions(self,destination_place_id):
        response = requests.get(self.url_directions + str(self.lat) + "," + str(self.long) + "&destination=place_id:" + str(
            destination_place_id) + "&waypoints=" )
obj=places()
obj.get_nearby_worship()
obj.get_nearby_charities()