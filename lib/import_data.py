import shutil, os.path, sys, platform, csv, codecs

import pandas as pd
import xrdtools

from lib import path_tools as pt

def init(flag, samples_dir):
    """
    This module should create the environment we want to work with when plotting/working with data. 

    This includes:
    -Local copy of all original data
    -Plot-ready data in scrap/*copy*/plt_data
    -Receptacle for figures in scrap/*copy*/output

    It should return a pandas DataFrame with scan data too.
    """

    # Checks whether multiple sample directories were passed as list
    # Currently not planning on implementing this
    if isinstance(samples_dir, str) == True:
        pt.init(flag, samples_dir)
    elif isinstance(samples_dir, list) == True:
        for folder in samples_dir:
            pt.init(flag, folder)
    else:
        sys.exit("ERROR: Invalid value in samples_dir.")

    if flag == "xrd":
        data = readXRD(os.path.join(scrap_dir, "XRD", samples_dir))
    elif flag == "pl":
        data = readPL(os.path.join(scrap_dir, "PL", samples_dir))
    elif flag == "uvvis":
        data = readUVVIS(os.path.join(scrap_dir, "UVVIS", samples_dir))
    elif flag == "ftir":
        data = readFTIR(os.path.join(scrap_dir, "FTIR", samples_dir))
    else:
        sys.exit("ERROR: Functionality not yet developed.")

    return data

def readXRD(sample_scrap_dir):
    """
    -Takes location of local copy of data and extracts python-readable data from XRDML files

    -Had to create dummy variable correct_items to remove unwanted files first
    -Correct list is reassigned to scrap_contents after 
    """

    scrap_contents = os.listdir(sample_scrap_dir)

    # Check for desired filetype, if not move to junk folder
    for item in scrap_contents:
        if (
            os.path.isfile(sample_scrap_dir + item) == True and 
            item.lower().endswith(".xrdml") == False
        ):
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "junk/")
        else:
            pass
    
    # Update scrap folder contents after cleaning
    scrap_contents = os.listdir(sample_scrap_dir)
    
    """
    This section:
    -Iterate over files we want to extract data from now
    -Clean filenames to make easier descriptors later 
    -Raw data is placed into scrap/*sample*/raw
    -Data is spat out into csv files in scrap/*sample*/py_data
    """

    # Initialize scan_data dict that will contain key-assigned data that is later fed into pandas DataFrame
    scan_data = {}

    # List useless XRD scan names that need to be cleaned
    useless_exts = [
        " Tomas_quick gonio scan_1",
        " Tomas_long gonio scan_2"
    ]

    #Clean XRDML filenames to make plot labeling easier later
    for item in scrap_contents:
        for ext in useless_exts:
            if ext in item:
                newname = item.replace(ext, "")
                os.rename(sample_scrap_dir + item, sample_scrap_dir + newname)
    
    # Update scrap folder contents after cleaning filenames
    scrap_contents = os.listdir(sample_scrap_dir)

    # Read all details extracted by xrdtools into scan_data dict
    for item in scrap_contents:
        if (
            os.path.isfile(sample_scrap_dir + item) == True and
            item.startswith("CIF") != True   
        ):
            scan_data[item] = xrdtools.read_xrdml(sample_scrap_dir + item)
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "raw/")
            
        else:
            pass

    clean_key_data = {}

    for key in scan_data.keys():
        clean_key_data[key.replace(".xrdml","")] = scan_data[key]
    
    """
    This section:
    -Takes dict data and outputs .csv files
    -Returns a dict of pandas DataFrames
    """

    # Dict of pandas DataFrames of entire sample pool indexed by clean keys
    meta_export_table = {}

    for key in clean_key_data.keys():
        export_table = pd.DataFrame(data=None, columns=["2theta", "counts"])

        export_table["2theta"] = clean_key_data[key]["x"]
        export_table["counts"] = clean_key_data[key]["data"]

        export_table.to_csv(
            os.path.join(sample_scrap_dir, "py_data/")
            + key
            + ".csv",
            index=False)

        meta_export_table[key] = export_table
        del export_table

    return meta_export_table

def readPL(sample_scrap_dir):
    """
    -Takes location of local copy of data and extracts python-readable data from XRDML files

    -Had to create dummy variable correct_items to remove unwanted files first
    -Correct list is reassigned to scrap_contents after 
    """

    scrap_contents = os.listdir(sample_scrap_dir)

    # Check for desired filetype, if not move to junk folder
    for item in scrap_contents:
        if (
            os.path.isfile(sample_scrap_dir + item) == True and 
            item.lower().endswith(".txt") == False
        ):
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "junk/")
        else:
            pass
        
    # Update scrap folder contents after cleaning
    scrap_contents = os.listdir(sample_scrap_dir)
    
    """
    This section:
    -Iterate over files we want to extract data from now
    -Clean filenames to make easier descriptors later 
    -Raw data is placed into scrap/*sample*/raw
    -Data is spat out into csv files in scrap/*sample*/py_data
    """

    # Initialize scan_data dict that will contain key-assigned data that is later fed into pandas DataFrame
    scan_data = {}
    
    # Update scrap folder contents after cleaning filenames
    scrap_contents = os.listdir(sample_scrap_dir)

    # Read file directly into pandas DataFrame
    # TODO: find a way for the reading process to automatically ignore parameter header regardless of length
    for item in scrap_contents:
        if os.path.isfile(sample_scrap_dir + item):
            
            scan_data[item] = pd.read_csv(sample_scrap_dir + item, sep='\t',        skiprows=37, names=['wavelength', 'counts'])
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "raw/")

        else:
            pass
    
    # Cleans keys up a little for easy plot labeling
    clean_key_data = {}
    for key in scan_data.keys():
        clean_key_data[key.replace(".txt","")] = scan_data[key]
    
    return clean_key_data

def readUVVIS(sample_scrap_dir):
    """
    -Takes location of local copy of data and extracts python-readable data from XRDML files

    -Had to create dummy variable correct_items to remove unwanted files first
    -Correct list is reassigned to scrap_contents after 
    """

    scrap_contents = os.listdir(sample_scrap_dir)

    # Check for desired filetype, if not move to junk folder
    for item in scrap_contents:
        if (
            os.path.isfile(sample_scrap_dir + item) == True and 
            item.lower().endswith(".txt") == False
        ):
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "junk/")
        else:
            pass
        
    # Update scrap folder contents after cleaning
    scrap_contents = os.listdir(sample_scrap_dir)
    
    """
    This section:
    -Iterate over files we want to extract data from now
    -Clean filenames to make easier descriptors later 
    -Raw data is placed into scrap/*sample*/raw
    -Data is spat out into csv files in scrap/*sample*/py_data
    """

    # Initialize scan_data dict that will contain key-assigned data that is later fed into pandas DataFrame
    scan_data = {}
    
    # Update scrap folder contents after cleaning filenames
    scrap_contents = os.listdir(sample_scrap_dir)

    # Read file directly into pandas DataFrame
    for item in scrap_contents:
        if os.path.isfile(sample_scrap_dir + item):
            
            scan_data[item] = pd.read_csv(sample_scrap_dir + item, sep='\t',        skiprows=2, names=['wavelength', 'abs'])
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "raw/")

        else:
            pass
    
    # Cleans keys up a little for easy plot labeling
    clean_key_data = {}
    for key in scan_data.keys():
        clean_key_data[key.replace(".txt","")] = scan_data[key]
    
    return clean_key_data

def readFTIR(sample_scrap_dir):

    scrap_contents = os.listdir(sample_scrap_dir)

    # Check for desired filetype, if not move to junk folder
    for item in scrap_contents:
        if (
            os.path.isfile(sample_scrap_dir + item) == True and 
            item.lower().endswith(".csv") == False
        ):
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "junk/")
        else:
            pass
    
    # Update scrap folder contents after cleaning
    scrap_contents = os.listdir(sample_scrap_dir)
    
    """
    This section:
    -Iterate over files we want to extract data from now
    -Clean filenames to make easier descriptors later 
    -Raw data is placed into scrap/*sample*/raw
    -Data is spat out into csv files in scrap/*sample*/py_data
    """

    # Initialize scan_data dict that will contain key-assigned data that is later fed into pandas DataFrame
    scan_data = {}

    # Read all details extracted by xrdtools into scan_data dict
    for item in scrap_contents:
        if os.path.isfile(sample_scrap_dir + item) == True:
            scan_data[item] = pd.read_csv(sample_scrap_dir + item,
                names=['Cm-1', 'Counts'])
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "raw/")
        else:
            pass

    clean_key_data = {}

    for key in scan_data.keys():
        clean_key_data[key.replace(".CSV","")] = scan_data[key]
    
    """
    This section:
    -Takes dict data and outputs .csv files
    -Returns a dict of pandas DataFrames
    """

    # Dict of pandas DataFrames of entire sample pool indexed by clean keys
    meta_export_table = {}

    for key in clean_key_data.keys():
        export_table = pd.DataFrame(data=None, columns=["Cm-1", "Counts"])

        export_table["Cm-1"] = clean_key_data[key]["Cm-1"]
        export_table["Counts"] = clean_key_data[key]["Counts"]

        meta_export_table[key] = export_table
        del export_table

    return meta_export_table

# GLOBAL PLATFORM DEPENDENT VARIABLES
if platform.system() == "Darwin":
    working_dir = "/Users/tomas/Documents/sciencetools_py/"
else:
    working_dir = "/home/tomas/Documents/sciencetools_py/"

scrap_dir = os.path.join(working_dir, "scrap/")