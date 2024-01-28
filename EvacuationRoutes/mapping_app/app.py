
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import json
import pandas as pd
import requests
import geopandas as gpd
app = Flask(__name__)

markers = [{
  "coords":{'lat': 13.0103286, 'lng': 80.2488214},
  'iconImage':'http://maps.google.com/mapfiles/ms/icons/homegardenbusiness.png',
 'content':'<h3>Adayar Govt School</h3> <p>Contact at <a href=\\"tel:+917075657100\\">(707) 565-7100</a>.</p>'
},
{
'coords':{'lat':13.0166311, 'lng':80.2060891},
'iconImage':'http://maps.google.com/mapfiles/ms/icons/homegardenbusiness.png',
'content':'<h3>Saidapet Govt School</h3> <p>Contact at <a href=\\"tel:+917075657100\\">(707) 565-7100</a>.</p>'
},
{
'coords':{'lat':13.011115, 'lng':80.1977458},
'iconImage':'http://maps.google.com/mapfiles/ms/icons/homegardenbusiness.png',
'content':'<h3>Nandanam Govt School</h3> <p>Contact at <a href=\\"tel:+917075657100\\">(707) 565-7100</a>.</p>'
},
{
'coords':{'lat':13.0489049, 'lng':80.0728893},
'iconImage':'http://maps.google.com/mapfiles/ms/icons/homegardenbusiness.png',
'content':'<h3>Panimalar College</h3> <p>Contact at <a href=\\"tel:+917075657100\\">(707) 565-7100</a>.</p>'
},
{
'coords':{'lat':13.025393, 'lng':80.268286},
'iconImage':'http://maps.google.com/mapfiles/ms/icons/homegardenbusiness.png',
'content':'<h3>Casagrand Olympus</h3> <p>Contact at <a href=\\"tel:+917075657100\\">(707) 565-7100</a>.</p>'
}
]


# reading the road_closures csv
road = pd.read_csv('road_closures.csv')

#getting only the closed roads related to fire
road = road[road['status'].str.contains('Fire')]

#loops over the each closed road
# gets and formates the
road_geo = []
for i in road.road:

    i = i.replace(' ', '%20')
    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={i}&inputtype=textquery&fields=geometry&key=${API_KEY}'

    res = requests.get(url)
    go = res.json()
    # print(go)
    mo =go['candidates'][0]['geometry']['location']
    road_geo.append({"coords":mo, "iconImage" : 'http://maps.google.com/mapfiles/kml/shapes/caution.png'})

# print(road_geo)


fire_map = gpd.read_file('MODIS_C6_USA_contiguous_and_Hawaii_24h/')
fire_map_loc = []
for i,k in zip(fire_map['LATITUDE'],fire_map['LONGITUDE']):
    fire_map_loc.append({"coords" : {'lat' : i,'lng' : k }, 'iconImage' : 'http://maps.google.com/mapfiles/ms/icons/firedept.png'})


@app.route('/')
def hello_world():
    return render_template('dir.html', markers=json.dumps(markers), road_geo=json.dumps(road_geo), fire_map_loc=json.dumps(fire_map_loc))

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)


url = f'https://maps.googleapis.com/maps/api/geocode/json?address=Walmart+Falls+Church&key=${API_KEY}'
