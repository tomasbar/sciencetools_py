import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from lib import import_data
import pandas as pd

"""
The bulk of the plotting will be handled from here
"""

# Set the technique we're working with today
# Valid values: 'xrd', 'pl', 'uvvis'
flag = "xrd"

# Identify the folder(s) where the raw, original data is
# Use a list to store multiple directories that you want ready to plot
samples_dir = "190710 ETB-042 EDBE-PbBr on glass FF/"

data_dict = import_data.init(flag, samples_dir)
print(data_dict)
# import_data.wipe_scrap()