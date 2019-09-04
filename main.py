import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from lib import import_data
import pandas as pd

"""
The bulk of the plotting will be handled from here
"""
# import_data.wipe_scrap()

# Set the technique we're working with today
# Valid values: 'xrd', 'pl', 'uvvis'
flag = "xrd"

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

# print(data_dict_etb046)

for key in cypher_etb046:
    plt.plot(data_dict_etb046[key]["2theta"], data_dict_etb046[key]["counts"], label=key)

plt.xlabel("2θ [deg.]")
plt.ylabel("Counts")
plt.legend()

plt.title("MAPbI Film Formation XRD")

print('about to plot lul')
plt.show()
