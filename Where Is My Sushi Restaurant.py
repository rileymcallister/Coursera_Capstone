#!/usr/bin/env python
# coding: utf-8

# In[1]:


# My client would like to open a sushi restaurant in Houston, TX, but they haven't been able to choose a location.

# They think the best location will be where there is a high density of residents and a low density of existing
# sushi restaurants, i.e. more customers and fewer competitors. 

# My plan is to utilize Python programming to reveal some possible locations for the restaurant.


# In[2]:


# Install and import appropriate packages:

get_ipython().system('conda install -c conda-forge scikit-learn --yes')
get_ipython().system('conda install -c conda-forge lxml --yes')
get_ipython().system('conda install -c conda-forge geopy --yes')
get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')

import numpy as np
import pandas as pd
import json
import lxml

from IPython.display import Image 
from IPython.core.display import HTML 

from geopy.geocoders import Nominatim

import requests
from pandas.io.json import json_normalize

import matplotlib.cm as cm
import matplotlib.colors as colors
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans


import folium

print("Done.")


# In[3]:


# Set up Foursquare access:

CLIENT_ID = 'PVKFVTWRLLOZO0ADVKZZOEOFJUYFKELV0XADDQVALQTC0AJ0'
CLIENT_SECRET = 'PHTMQF32E1WH5DZXDKWKPFGCGC5JP3E1FEBRYCG323TQR5M4'
VERSION = '20180604'
LIMIT = 30

# The client does not want to commute more than 5000 meters from their place of residence, so we will begin with this address:
address = '5701 Main St, Houston, TX'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude

# Format Foursquare API query
QUERY = 'sushi'
RADIUS = 5000
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, QUERY, RADIUS, LIMIT)

# Get query results

results = requests.get(url).json()

# Then convert results into a pandas dataframe

sushi_venues = results['response']['venues']
sushi_venues = pd.DataFrame(sushi_venues)
sushi_venues.shape


# In[4]:


# Data Processing - Let's see if we can filter out irrelevant information:

# Keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories','location','id']
sushi_venues_filtered = sushi_venues.loc[:, filtered_columns]

# Function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# Filter the category for each row
sushi_venues_filtered['categories'] = sushi_venues_filtered.apply(get_category_type, axis=1)

# Clean column names by keeping only last term
sushi_venues_filtered.columns = [column.split('.')[-1] for column in sushi_venues_filtered.columns]

# Now let's retain only the restaurants that are classified as "Sushi Restaurant":

sushi_venues_filtered = sushi_venues_filtered[(sushi_venues_filtered['categories']=='Sushi Restaurant')]
sushi_venues_filtered.reset_index(drop=True,inplace=True)

# Now we're down to 19 restaurants!

sushi_venues_filtered


# In[5]:


# Now let's see our competitors on a map:

sushi_venues_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Add a red circle marker to represent our client's home

folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    color='green',
    popup='Client Home',
    fill = True,
    fill_color = 'green',
    fill_opacity = 0.6
).add_to(sushi_venues_map)

# Add the sushi restaurants as blue circle markers
for row in sushi_venues_filtered['location']:
    lat = row['lat']
    lng = row['lng']
    label = "Sushi Restaurant"
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(sushi_venues_map)

sushi_venues_map


# In[6]:


# Now we need to find some areas in the map that are not near any competitor sushi restaurants while still being close
# to the client's home. To do this, we will replace the CircleMaker points with Circle points; this way, we can create circles
# of a fixed radius length. The client has decided that they do not want their restaurant to be within 2 kilometers of any
# competitor.

for row in sushi_venues_filtered['location']:
    lat = row['lat']
    lng = row['lng']
    label = None
    folium.Circle(
        [lat, lng],
        radius=2000,
        color='red',
        popup=label,
        fill = True,
        fill_color='red',
        fill_opacity=0.3
    ).add_to(sushi_venues_map)

sushi_venues_map

# Now that the client has this map, they can begin exploring sites that are not within the red circles.


# In[ ]:




