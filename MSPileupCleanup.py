import json
import os

f = open("../WmAgentScripts/campaigns.json", "r")
campaigns = json.loads(f.read())

i = 0
pus = []
for campaign, config in campaigns.items():
    if "secondaries" in config.keys():
        for pu in config["secondaries"].keys():
            rucio_out = os.popen(f"rucio list-dataset-replicas cms:{pu}")
            print(rucio_out)

