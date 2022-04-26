import pandas as pd
import numpy as np
import folium
from folium import Marker
import geopandas as gpd
import warnings 
from geopy.geocoders import Nominatim
from shapely.geometry import Point
warnings.filterwarnings('ignore')
import webbrowser

def nearest_ag():
    geolocator = Nominatim(user_agent="rasa_chatbot")
    location = geolocator.geocode("PICOSOFT NEW HEADQUARTERS")
    data = {'Name': ['Esprit'], 'Latitude': [location.point.latitude], 'Longitude': [location.point.longitude]}
    dat = pd.DataFrame(data)
    pos = dat.apply(lambda row : Point(row.Longitude, row.Latitude), axis=1)
    position = gpd.GeoDataFrame(dat, geometry=pos)
    position.crs = {'init': 'epsg:4326'}
    loc = pd.read_csv(r"C:\Users\medez\Desktop\pi\agencies_locations.csv")
    l =['Name', 'Latitude', 'Longitude']
    locations = loc[l]
    agen = locations.apply(lambda row : Point(row.Longitude, row.Latitude), axis=1)
    agencies = gpd.GeoDataFrame(locations, geometry=agen)
    agencies.crs = {'init': 'epsg:4326'}
    p = position.iloc[0]
    distances = agencies.geometry.distance(p.geometry)
    m = folium.Map(location=[36, 10], tiles='openstreetmap', zoom_start=7)
    folium.Marker(location = [loc.iloc[distances.idxmin()].Latitude, loc.iloc[distances.idxmin()].Longitude]).add_to(m)
    return m
