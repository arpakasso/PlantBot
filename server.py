#!/usr/bin/python3
"""
File: server.py
Author: Elizabeth Trinh
Purpose:
	Takes requests and returns data relating to the request.
"""

from flask import Flask, request
import os
import requests
import json
from df_response_lib import fulfillment_response
import re
from User import User
import pickle


app = Flask(__name__)
user = User()
plant_list = dict()
plant_db = dict()

@app.route('/')
def serve_homepage():
    return 'homepage'


def serve_zone(param):
    city = param.get('geo-city') or ""
    state = param.get('geo-state-us') or ""
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+city+","+state+"&location_type=GEOMETRIC_CENTER&key="+os.environ['maps_api_key']
    geocode_resp = json.loads(requests.post(geocode_url).text)
    lat = geocode_resp['results'][0]['geometry']['location']['lat']
    lng = geocode_resp['results'][0]['geometry']['location']['lng']
    rev_geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(lng)+"&key="+os.environ['maps_api_key']
    rev_geocode_resp = json.loads(requests.post(rev_geocode_url).text)
    components = rev_geocode_resp['results'][0]['address_components']
    zip_code = "75080"
    for comp in components:
        if 'postal_code' in comp['types']:
            zip_code = comp['long_name']
    zone_url = "https://phzmapi.org/"+zip_code+".json"
    zone_resp = json.loads(requests.get(zone_url).text)
    zone = re.sub('[^0-9]', '', zone_resp['zone'])
    user.set_zone(zone)
    return "You live in Zone " + zone


def serve_plant_types():
    return 'plant type'


def serve_plant(param):
    plant = param.get('specificplants')
    if plant in plant_list.keys():
        return plant_list[plant].get_data()[""][2]
    else:
        return "Sorry, I don't know much about " + plant.lower()



@app.route('/webhook', methods=['POST'])
def serve_webhook():
    fr = fulfillment_response()
    # build a request object
    req = request.get_json(force=True)
    print(req)
    # fetch action from json
    resp = "brokoro"
    intent = req.get('queryResult').get('intent').get('displayName')
    parameters = req.get('queryResult').get('parameters')
    if intent == "find.zone.getlocation":
        resp = fr.fulfillment_text(serve_zone(parameters))
    elif intent == "get.specificplant":
        resp = fr.fulfillment_text(serve_plant(parameters))
    else:
        resp = fr.fulfillment_text(resp)
    # return a fulfillment response
    return json.dumps(fr.main_response(fulfillment_text=resp))


if __name__ == '__main__':
    plantpages = open('plantpages.pkl', 'rb')
    plant_list = pickle.load(plantpages)
    plantpages.close()

    plantdb = open('plantdb.pkl', 'rb')
    plant_db = pickle.load(plantdb)
    plantdb.close()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
    # app.run(threaded=True)