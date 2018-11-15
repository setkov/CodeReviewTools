
import TfsApi
import json


configPath = "CodeReviewTools.json"


# read configuration file
with open(configPath, 'r') as configFile:
    config = json.load(configFile)


