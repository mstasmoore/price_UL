# import necessary libraries
# from models import create_classes
import os
from math import sin, cos, sqrt, atan2, radians

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, or_
from sqlalchemy.ext.automap import automap_base
from geopy.geocoders import Nominatim

import pickle

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from flask_cors import CORS

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)
# ---------------------------------------------------------
# Web site

class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

@app.route("/api/prediction/<origin>/<destination>/<weather>/<vehicleType>/<weekDay>" , methods=["GET"])
def model(origin, destination, weather, vehicleType, weekDay):

    origin_text = origin.replace('_', ' ')
    #address we need to geocode
    loc_origin = origin_text + ', Boston, Massachusetts'
    #making an instance of Nominatim class
    geolocator = Nominatim(user_agent="my_request")
    #applying geocode method to get the location
    location_origin = geolocator.geocode(loc_origin)
 
    destination_text = destination.replace('_', ' ')
    #address we need to geocode
    loc_destination = destination_text + ', Boston, Massachusetts'
    #making an instance of Nominatim class
    geolocator = Nominatim(user_agent="my_request")
    #applying geocode method to get the location
    location_destination = geolocator.geocode(loc_destination)

    R = 6373.0

    lat1 = radians(location_origin.latitude)
    lon1 = radians(location_origin.longitude)
    lat2 = radians(location_destination.latitude)
    lon2 = radians(location_destination.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    total_distance = R * c

    print("Result:", total_distance)

    distance = total_distance
    Monday = 0
    Tuesday = 0
    Wednesday = 0
    Thursday = 0
    Friday = 0
    Saturday = 0
    Sunday = 0

    while switch(weekDay):
        if case('Monday'):
            Monday = 1
            break
        if case ('Tuesday'):
            Tuesday = 1
            break
        if case ('Wednesday'):
            Wednesday = 1
            break
        if case ('Thursday'):
            Thursday = 1
            break  
        if case ('Friday'):
            Friday = 1
            break
        if case ('Saturday'):
            Saturday = 1
            break
        if case ('Sunday'):
            Sunday = 1
            break
    
    Mostly_Cloudy = 0
    Rain = 0
    Partly_Cloudy = 0 
    Clear = 0
    Overcast = 0
    Light_Rain = 0
    Foggy = 0
    Possible_Drizzle = 0
    Drizzle = 0

    while switch(weather):
        if case('Mostly_Cloudy'):
            Mostly_Cloudy = 1
            break
        if case ('Rain'):
            Rain = 1
            break
        if case ('Partly_Cloudy'):
            Partly_Cloudy = 1
            break
        if case ('Clear'):
            Clear = 1
            break  
        if case ('Overcast'):
            Overcast = 1
            break
        if case ('Light_Rain'):
            Light_Rain = 1
            break
        if case ('Foggy'):
            Foggy = 1
            break
        if case ('Possible_Drizzle'):
            Possible_Drizzle = 1
            break
        if case ('Drizzle'):
            Drizzle = 1
            break

    UberPool = 0
    UberXL = 0
    Black = 0
    Black_SUV = 0
    WAV = 0
    UberX = 0

    Shared = 0
    LyftXL = 0
    Lux_Black = 0
    Lux_Black_XL = 0
    Lux = 0
    Lyft = 0
    
    while switch(vehicleType):
        if case('UberPool-Shared'):
            UberPool = 1
            Shared = 1
            break
        if case ('UberXL-LyftXL'):
            UberXL = 1
            LyftXL = 1
            break
        if case ('Black-Lux_Black'):
            Black = 1
            Lux_Black = 1
            break
        if case ('Black_SUV-Lux_Black_XL'):
            Black_SUV = 1
            Lux_Black_XL = 1
            break  
        if case ('UberX-Lyft'):
            UberX = 1
            Lyft = 1
            break
        if case ('WAV-Lux'):
            WAV = 1
            Lux = 1
            break
        
    prediction_u = 0
    prediction_l = 0

    X_u = [[distance, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday,
          UberPool, UberXL, Black, Black_SUV, WAV, UberX, Mostly_Cloudy, Rain, Partly_Cloudy, 
          Clear, Overcast, Light_Rain, Foggy, Possible_Drizzle, Drizzle]]

    X_l = [[distance, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday,
          Shared, LyftXL, Lux_Black, Lux_Black_XL, Lux, Lyft, Mostly_Cloudy, Rain, Partly_Cloudy, 
          Clear, Overcast, Light_Rain, Foggy, Possible_Drizzle, Drizzle]]
    
    print(X_u)
    print(X_l)

    filename_u = './data/u_model.sav'
    loaded_model_u = pickle.load(open(filename_u, 'rb'))

    print(loaded_model_u.predict(X_u))
    
    prediction_u = loaded_model_u.predict(X_u)[0]

    print(prediction_u)

    filename_l = './data/l_model.sav'
    loaded_model_l = pickle.load(open(filename_l, 'rb'))

    print(loaded_model_l.predict(X_l))
    
    prediction_l = loaded_model_l.predict(X_l)[0]

    print(prediction_l)

    type_car = 'Same price for Uber and Lyft'
    price = prediction_u
    
    if prediction_u < prediction_l:
        type_car = 'Uber'
        price = prediction_u
    else:
        type_car = 'Lyft'
        price = prediction_l

    results = {
        "type": type_car,
        "price":  "${0:,.2f}".format(price)
    }
    print(results)
    return jsonify(results)


if __name__ == "__main__":
    app.run()
