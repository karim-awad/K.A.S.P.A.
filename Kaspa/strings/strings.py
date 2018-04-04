import glob
import json
from Kaspa.config import Config

BASE_PATH = "Kaspa/strings/"


def get_strings(class_name):
    config = Config.get_instance()
    language = config.get("general", "language")
    path = glob.glob(BASE_PATH + language + "/**/" + class_name + "*", recursive=True)
    file = open(path[0], "r")
    strings = json.load(file)
    file.close()
    return strings
