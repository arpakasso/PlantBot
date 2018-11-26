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
    text = "You live in Zone "+zone
    return zone, text


def serve_plant_types(param):
    zone = user.get_zone()
    if zone == "":
        zone = serve_zone({'geo-city':param.get('geo-city'), 'geo-state-us':param.get('geo-state-us')})
    zone_plants = plant_db['Hardiness Zones'][zone]
    plant_types_plants = plant_db['Plant Type'][param.get('Plant_Types')]
    relevant_plants = intersection(zone_plants, plant_types_plants)
    return "You can plant " + ", ".join(relevant_plants).lower() + " in " + param.get('geo-city') + ", " + param.get('geo-state-us')


def serve_plant(param):
    plant = param.get('specificplants')
    if plant in plant_list.keys():
        return plant_list[plant].get_data()[""][2]
    else:
        return "Sorry, I don't know much about " + plant.lower()


def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]


@app.route('/webhook', methods=['POST'])
def serve_webhook():
    fr = fulfillment_response()
    # build a request object
    req = request.get_json(force=True)
    print(req)
    # fetch action from json
    resp = "brokoro"
    zone = None
    intent = req.get('queryResult').get('intent').get('displayName')
    parameters = req.get('queryResult').get('parameters')
    if intent == "find.zone.getlocation":
        zone, text = serve_zone(parameters)
        resp = fr.fulfillment_text(text)
    elif intent == "get.specificplant" or intent == "plant.info.specific":
        resp = fr.fulfillment_text(serve_plant(parameters))
    elif intent == "suggestplants.locationknown" or intent == "suggestplants.fulfill":
        parameters = req.get('queryResult').get('outputContexts')[0].get('parameters')
        resp = fr.fulfillment_text(serve_plant_types(parameters))
    # elif intent == "listplants.getlocation":
    #
    else:
        resp = fr.fulfillment_text(resp)
    # return a fulfillment response
    req.get('queryResult')['fulfillmentText'] = resp
    req.get('queryResult').get('fulfillmentMessages')[0].get('text').get('text')[0] = resp
    # return json.dumps(fr.main_response(fulfillment_text=resp))
    return json.dumps(req)


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