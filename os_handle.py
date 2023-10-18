import os 
import json

#current directory, used for creation of results
cur_dir=os.getcwd()

def ch_cr(path):
    """
    Check is directory exist
    Create directory by folow path if dont
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def config_load():
    """Loads config from config.json file"""
    with open("config.json", "r", encoding="utf-8") as file:
        config=json.load(file)
    return config["lector_radar"], config["practice_radar"], \
           config["histogram_y"], config["histogram_11_name"], config["histogram_12_name"]