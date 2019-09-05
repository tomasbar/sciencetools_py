#!/usr/bin/env python
# coding: utf-8

# In[32]:


import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from lib import import_data

# In[23]:


import_data.wipe_scrap()

# Set the technique we're working with today
# Valid values: 'xrd', 'pl', 'uvvis'
flag = "xrd"


# In[24]:


# Identify the folder(s) where the raw, original data is
# Use a list to store multiple directories that you want ready to plot

# ETB-046 Variables
samples_dir_etb046 = "190722 ETB-046 MAPbI on glass FF/"
data_dict_etb046 = import_data.init(flag, samples_dir_etb046)
cypher_etb046 = (
    "30sec",
    "1min",
    "2min",
    "3min",
    "5min",
    "20min",
)


# In[25]:


# ETB-047 Variables
samples_dir_etb047 = "190903 ETB-047 MAPbI on glass FF/"
data_dict_etb047 = import_data.init(flag, samples_dir_etb047)
print(data_dict_etb047.keys())
cypher_etb047 = (
    "10min",
    "40min",
    "60min",
    "80min",
    "100min",
    "120min",
)


# In[26]:


# ETB-048 Variables
samples_dir_etb048 = "190904 ETB-048 MAPbI on glass FF/"
data_dict_etb048 = import_data.init(flag, samples_dir_etb048)
print(data_dict_etb048.keys())

cypher_etb048 = (
    "4min",
    "15min",
)


# In[136]:


fig = plt.figure(1)
fig_ax = plt.gca()

offset = 0
master_cypher = (
    "30sec",
    "1min",
    "2min",
    "3min",
    "4min",
    "5min",
    "10min",
)

for key in master_cypher:
    if key in data_dict_etb046.keys():
        plt.figure(1)
        plt.plot(data_dict_etb046[key]["2theta"], data_dict_etb046[key]["counts"] + offset,
                 label=key)
        offset += max(data_dict_etb046[key]["counts"])
    elif key in data_dict_etb047.keys():
        plt.figure(1)
        plt.plot(data_dict_etb047[key]["2theta"], data_dict_etb047[key]["counts"] + offset,
                 label=key)
        offset += max(data_dict_etb047[key]["counts"])
    elif key in data_dict_etb048.keys():
        plt.figure(1)
        plt.plot(data_dict_etb048[key]["2theta"], data_dict_etb048[key]["counts"] + offset,
                 label=key)
        offset += max(data_dict_etb048[key]["counts"])

plt.style.use('default')

plt.xlabel("2θ [degrees]", weight="semibold")
plt.ylabel("Counts", weight="semibold")
fig_ax.set_yticklabels([])
plt.xlim(min(data_dict_etb046["1min"]["2theta"]), max(data_dict_etb046["1min"]["2theta"]))

plt.title("MAPbI Film Formation XRD - Early Stages",weight="semibold")
plt.legend(loc='center left', bbox_to_anchor=(1.01, 0,.22,1),mode='expand', frameon=False)

