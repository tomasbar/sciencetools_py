import shutil
import os.path
import sys
import platform
import csv

import xrdtools
import pandas as pd

working_dir = "/Users/tomas/Documents/sciencetools_py/"
scrap_dir = working_dir + "scrap/"

def init(flag, samples_dir):
    """
    This module should create the environment we want to work with when plotting/working with data.

    This includes:
    -Local copy of all original data
    -Plot-ready data in scrap/*copy*/plt_data
    -Receptacle for figures in scrap/*copy*/output
    """

    # Checks whether multiple sample directories were passed
    if isinstance(samples_dir, str) == True:
        path_init(flag, samples_dir)
    elif isinstance(samples_dir, list) == True:
        for folder in samples_dir:
            path_init(flag, folder)
    else:
        sys.exit("ERROR: Invalid value in samples_dir.")

    if flag == "xrd":
        readXRD(scrap_dir + samples_dir)
    else:
        sys.exit("ERROR: Functionality not yet developed.")

def readXRD(sample_scrap_dir):
    """
    -Takes location of local copy of data and extracts python-readable data from XRDML files

    -Had to create dummy variable correct_items to remove unwanted files first
    -Correct list is reassigned to scrap_contents after 
    """
    scrap_contents = os.listdir(sample_scrap_dir)
    # correct_items = scrap_contents[:]

    for item in scrap_contents:
        if (
            os.path.isfile(sample_scrap_dir + item) == True and 
            item.lower().endswith(".xrdml") == False
        ):
            # correct_items.remove(item)
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "junk/")
        else:
            pass
    
    scrap_contents = os.listdir(sample_scrap_dir)
    print(scrap_contents)
    
    """
    This section:
    -Iterate over files we want to extract data from now
    -Clean filenames to make easier descriptors later 
    -Raw data is placed into scrap/*sample*/raw
    -Data is spat out into csv files in scrap/*sample*/py_data
    """
    scan_data = {}
    #Clean filenames
    for item in scrap_contents:
        newname = item.replace(" Tomas_quick gonio scan_1", "")
        os.rename(sample_scrap_dir + item, sample_scrap_dir + newname)
    
    scrap_contents = os.listdir(sample_scrap_dir)
    print(scrap_contents)

    for item in scrap_contents:
        if (
            os.path.isfile(sample_scrap_dir + item) == True and
            item.startswith("CIF") != True   
        ):
            print("reading " + item)
            shutil.move(sample_scrap_dir + item, sample_scrap_dir + "raw/")
            scan_data[item] = xrdtools.read_xrdml(sample_scrap_dir + "raw/" + item)
        else:
            print("skipped " + item)
            pass

    clean_key_data = {}

    for key in scan_data.keys():
        clean_key_data[key.replace(".xrdml","")] = scan_data[key]

    # print(clean_key_data.keys())
    # print(clean_key_data["20min"])
    
    # """
    # This section:
    # -Takes dict data and outputs .csv files
    # """
    # for sample in clean_key_data:
    #     with open(
    #         sample_scrap_dir + "/py_data/" + sample.key() + ".csv",
    #         mode="w"
    #     ) as csv_file:
    #         fieldnames = ["2theta", "counts"]
    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
    #         writer.writeheader()
    #         writer.writerows()

    export_table = pd.DataFrame(data=None, columns=["2theta", "counts"])

    for key in clean_key_data.keys():
        export_table["2theta"] = clean_key_data[key]["x"]
        export_table["counts"] = clean_key_data[key]["data"]

        export_table.to_csv(sample_scrap_dir + "py_data/" + key + ".csv",
            index=False)

    print(export_table)


def path_init(flag, head):
    """
    -Constructs path to folder of characterization method depending on flag
    -Checks validity of path constructed
    -Makes local copy of desired folder to work on
    """
    
    # Dictionary contains flag-directory pairs for all techniques, systems
    if platform.system() == "Darwin":
        box_root = "/Users/tomas/Box/Home Folder etb14/"
        cypher = {
            'xrd': (box_root + "XRD/"),
            'pl': (box_root + "PL/"),
            'uvvis': (box_root + "UV-VIS/"),
        }
    else:
        cypher = {
            'xrd': ("/home/tomas/Documents/data/Box/XRD/"),
            'pl': ("/home/tomas/Documents/data/Box/PL/"),
            'uvvis': ("/home/tomas/Documents/data/Box/UV-VIS/"),
        }

    # Check valid flag was passed, if valid construct path
    if flag in cypher.keys():
        path = cypher[flag] + head
    else:
        sys.exit("ERROR: Invalid flag provided, check 'flag' variable in import_main.py")
    
    # Check validity of constructed path
    if os.path.isdir(path) == False:
        sys.exit("ERROR: Invalid directory name, check samples_dir variable.")
    else:
        pass

    """
    Next section:
    -Empties given samples local scrap folder, if it exists already
    -Makes local copy of given 'path' in scrap folder
    """

    scrap_sample_dir = scrap_dir + head
    
    # Checks for presence of corresponding data in 'scrap' folder
    # Checks if new data should be overwritten whatever is in there already
    if os.path.isdir(scrap_sample_dir):
        if os.listdir(scrap_sample_dir) != []:
            
            rm = input("Sample data already in local memory, do you wish to wipe and pull from the master Box directory? y/n\n")
            
            if rm == "y":
                shutil.rmtree(scrap_sample_dir)
                shutil.copytree(path, scrap_sample_dir)
                populate_scrap(scrap_sample_dir)

            elif rm == "n":
                pass

        else:
            print("Empty folder found, repopulating now.")
            shutil.rmtree(scrap_sample_dir)
            shutil.copytree(path, scrap_sample_dir)
            populate_scrap(scrap_sample_dir)

        
    elif os.path.isdir(scrap_sample_dir) == False:
        print("Creating new local data folder.")
        shutil.copytree(path, scrap_sample_dir)
        populate_scrap(scrap_sample_dir)
        
def populate_scrap(scrap_sample_dir):
    os.mkdir(scrap_sample_dir + "junk/")
    os.mkdir(scrap_sample_dir + "py_data/")
    os.mkdir(scrap_sample_dir + "figures/")
    os.mkdir(scrap_sample_dir + "raw/")

def wipe_scrap():
    scrap_contents = os.listdir("./scrap")
    
    for folder in scrap_contents:
        shutil.rmtree("./scrap/" + folder)