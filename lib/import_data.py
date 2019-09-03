import shutil
import os.path
import sys

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

def path_init(flag, head):
    """
    -Constructs path to folder of characterization method depending on flag
    -Checks validity of path constructed
    -Makes local copy of desired folder to work on
    """
    
    # Dictionary contains flag-directory pairs for all techniques
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

    scrap_dir = "../scrap" + head
    
    # Checks for presence of corresponding data in 'scrap' folder
    # Checks if new data should be overwritten whatever is in there already
    if os.path.isdir(scrap_dir):
        if os.listdir(scrap_dir) != []:
            
            rm = input("Sample data already in local memory, do you wish to wipe and pull from the master Box directory? y/n\n")
            
            if rm == "y":
                shutil.rmtree(scrap_dir)
                shutil.copytree(path, scrap_dir)
            elif rm == "n":
                pass

        else:
            print("Empty folder found, repopulating now.")
            shutil.rmtree(scrap_dir)
            shutil.copytree(path, scrap_dir)
        
    elif os.path.isdir(scrap_dir) == False:
        print("Creating new local data folder.")
        shutil.copytree(path, scrap_dir)
    
def wipe_scrap():
    scrap_contents = os.listdir("./scrap")
    
    for folder in scrap_contents:
        shutil.rmtree("./scrap/" + folder)