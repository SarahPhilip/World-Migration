import os

import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import select

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from pprint import pprint
from operator import itemgetter
app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/MigrationData.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Mydata = Base.classes.mydata


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/maps")
def maps():
    df = pd.read_csv('cleanedData.csv')

    # select_data_2017 = select([Mydata]).where(Mydata.Year=='2017')
    # result = conn.execute(select_data_2017)
    result = db.session.query(Mydata.Year).filter(Mydata.Year == '2017').all()
    # Creating list of dictionaries where year = 2017
    resultset = []
    for row in result:
        resultset.append(dict(row))
    # Removing null values     
    newset = []
    for res in resultset:
        r = {k: v for k, v in res.items() if v != '..'}
        newset.append(r)
    # Creating list of dictionaries with destination, origin countries, ..
    data_2017 = []
    for res in resultset:
        select_data_2017 = {}
        select_data_2017['destination'] = res.pop('Destination',None)
        if select_data_2017['destination']  == None:
            continue
        select_data_2017['year'] = res.pop('Year',None)
        select_data_2017['code'] = res.pop('Code',None)
        select_data_2017['index'] = res.pop('index',None)
        select_data_2017['origin'] = {k: v for k, v in res.items() if v != '..'}
        if select_data_2017['origin']  == None:
            continue
        data_2017.append(select_data_2017) 

    # Finding all country codes
    country_code = []
    for value in session.query(Mydata.Code).distinct():
         for index, row in df.iterrows():
            if value[0] == row['Code']:
                p = {}
                p['code'] = row['Code']
                p['country'] = row['Destination']
                country_code.append(p) 

    # Finding unique country codes
    unique_country_codes = []

    for c in country_code:
        if c not in unique_country_codes:
            if {k: v for k, v in c.items() if v is not None}:
                unique_country_codes.append(c)

    # Find country code by name
    def getCountryCode(country):
        for c in country_code:
            for k,v in c.items():
                if v == country:
                    return c['code']

    # Get latitude from country code
    def getLatLng(country):
        code = int(getCountryCode(country))
    #     print(code)
        for l in latlng:
            for k, v in l.items():
                if v == code:
                    return [l['longitude'], l['latitude']]

        # Create JSON File which countains country code, name , latitude and longitude
    # Create JSON File which countains country code, name , latitude and longitude
    df_lat_long = pd.read_csv('Country_Codes_Latitude_Longitude.csv')
    latlng = []
    for value in session.query(Mydata.Code).distinct():
         for index, row in df_lat_long.iterrows():
            if value[0] == row['Numeric code']:
                p = {}
                p['code'] = row['Numeric code']
                p['country'] = row['Country']
                p['latitude'] = row['Latitude (average)']
                p['longitude'] = row['Longitude (average)']
                latlng.append(p)
    with open("latlng.json","w") as f:
        json.dump(latlng,f)

    # Color code according to number of migrants
    def getcolor(migrants):
    #     migrants = int(migrants.replace(',', ''))
        if migrants >= 100000:
            return "#d7191c"
        elif migrants < 100000 and migrants >= 50000:
            return "#fdae61"
        elif migrants < 50000 and migrants >= 10000:
            return "#ffffbf"
        elif migrants < 10000 and migrants >= 1000:
            return "#abdda4"
        else:
            return "#2b83ba"
        
    # Create dictionary for using in the plugin
    data_for_plugin_2017 = []
    for d in data_2017:
        data_dict = {}
        for k, v in d['origin'].items():
            data_dict['from'] = getLatLng(d['destination']) 
            if data_dict['from'] is None:
                data_dict = {}
                continue
    #         print(k)
            data_dict['to'] = getLatLng(k)
    #         data_dict['labels'] = [d['destination'], k]
            v = int(v.replace(',', ''))
            data_dict['color'] = getcolor(v) 
            data_dict['migrants'] = v
            data_dict['arcWidth'] = 0.1
            data_dict['pulseBorderWidth'] = 0.15
            data_dict['year'] = d['year']
    #         print(data_dict['from'])
            for k1, v1 in data_dict.items():
                if data_dict['from'] is not None:              
                    data_for_plugin_2017.append(data_dict)


    list_2 = []

    for d in data_for_plugin_2017:
        for k1, v1 in d.items():
                if d['to'] is not None: 
                    if d not in list_2:             
                        list_2.append(d)

# with open("data_for_plugin_2015.json","w") as f:
#     json.dump(list_2,f)



    # Return a list of the column names (sample names)
    return jsonify(list_2)


if __name__ == "__main__":
    app.run()
