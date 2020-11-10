#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[49]:


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

