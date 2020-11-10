#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Install and import appropriate packages and print "Done." when this is complete.

get_ipython().system('conda install -c conda-forge scikit-learn --yes')
get_ipython().system('conda install -c conda-forge lxml --yes')
get_ipython().system('conda install -c conda-forge geopy --yes')
get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')

import numpy as np
import pandas as pd
import json
import lxml

from geopy.geocoders import Nominatim

import requests
from pandas.io.json import json_normalize

import matplotlib.cm as cm
import matplotlib.colors as colors

from sklearn.cluster import KMeans


import folium

print("Done.")


# In[3]:


# Scrape wikipedia to create a dataframe with rows missing 'Borough' values removed.

wiki_dfs = pd.read_html("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
#filtered_columns = ["PostalCode","Borough","Neighborhood"]
#wiki_df = wiki_df.loc[:, filtered_columns]
wiki_df = pd.concat(wiki_dfs)
wiki_df = wiki_df[["Postal Code","Borough","Neighbourhood"]]
wiki_df.replace(to_replace="Not assigned", value=np.NaN, inplace=True)
wiki_df.dropna(axis=0, subset=["Borough"], inplace=True)
wiki_df.reset_index(drop=True)

# Set 'Neighborhood' values to equal 'Borough' values when missing.
wiki_df['Neighbourhood'].fillna(wiki_df['Borough'])

# Shape of dataframe

wiki_df.shape


# In[4]:


lat_lng_df = pd.read_csv("https://cocl.us/Geospatial_data")
lat_lng_df.head()


# In[6]:


# Merge Lat/long DF with wiki DF

merged_df = wiki_df.merge(lat_lng_df,how='left')
merged_df


# In[8]:


# Map of Downtown Toronto using latitude and longitude values
latitude = 43.665860
longitude = -79.383160

map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighbourhood in zip(merged_df['Latitude'], merged_df['Longitude'], merged_df['Borough'], merged_df['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# In[ ]:




