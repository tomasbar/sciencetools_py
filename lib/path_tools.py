import os, platform, sys, shutil

def init(flag, head):
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
        
        box_root = "/home/tomas/Documents/data/Box/"
        cypher = {
            'xrd': (box_root + "XRD/"),
            'pl': (box_root + "PL/"),
            'uvvis': (box_root + "UV-VIS/"),
        }

    # Check valid flag was passed, if valid construct path
    if flag in cypher.keys():
        box_path = os.path.join(cypher[flag], head)
    else:
        sys.exit("ERROR: Invalid flag provided, check 'flag' variable in import_main.py")
    
    # Check validity of constructed path
    if os.path.isdir(box_path) == False:
        sys.exit("ERROR: Invalid directory name, check samples_dir variable.")
    else:
        pass

    """
    Next section:
    -Empties given samples local scrap folder, if it exists already
    -Makes local copy of given 'path' in scrap folder
    """

    if flag == 'xrd':
        scrap_sample_dir = os.path.join(scrap_dir, "XRD/", head)
    elif flag == 'pl':
        scrap_sample_dir = os.path.join(scrap_dir, "PL/", head)
    elif flag == 'uvvis':
        scrap_sample_dir = os.path.join(scrap_dir, "UVVIS/", head)
      
    # Checks for presence of corresponding data in 'scrap' folder
    # Checks if new data should be overwritten whatever is in there already
    if os.path.isdir(scrap_sample_dir):
        if os.listdir(scrap_sample_dir) != []:
            
            rm = input("\nSample data already in local memory, do you wish to wipe and pull from the master Box directory? y/n\n")
            
            if rm == "y":
                shutil.rmtree(scrap_sample_dir)
                shutil.copytree(box_path, scrap_sample_dir)
                populate_scrap(scrap_sample_dir)

            elif rm == "n":
                print("\nContinuing with already imported data.\n")
                pass

        else:
            print("\nEmpty folder found, repopulating now.\n")
            shutil.rmtree(scrap_sample_dir)
            shutil.copytree(box_path, scrap_sample_dir)
            populate_scrap(scrap_sample_dir)

        
    else:
        print("Creating new local data folder.")    
        shutil.copytree(box_path, scrap_sample_dir)
        populate_scrap(scrap_sample_dir)
        
def populate_scrap(scrap_sample_dir):
    os.mkdir(os.path.join(scrap_sample_dir, "junk/"))
    os.mkdir(os.path.join(scrap_sample_dir, "py_data/"))
    os.mkdir(os.path.join(scrap_sample_dir, "figures/"))
    os.mkdir(os.path.join(scrap_sample_dir, "raw/"))

def wipe_scrap():
    scrap_contents = os.listdir("./scrap")
    
    for folder in scrap_contents:
        shutil.rmtree(os.path.join("./scrap/", folder))

# GLOBAL PLATFORM DEPENDENT VARIABLES
if platform.system() == "Darwin":
    working_dir = "/Users/tomas/Documents/sciencetools_py/"
else:
    working_dir = "/home/tomas/Documents/sciencetools_py/"

scrap_dir = os.path.join(working_dir, "scrap/")