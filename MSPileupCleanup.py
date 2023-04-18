import json
import os
from collections import OrderedDict

f = open("../WmAgentScripts/campaigns.json", "r")
campaigns = json.loads(f.read(), object_pairs_hook=OrderedDict)

i = 0
pus = []
pus_to_clean = []
for campaign, config in campaigns.items():
    if "secondaries" in config.keys():
        for pu in config["secondaries"].keys():
            pus.append(pu)
            rucio_out = os.popen("rucio list-dataset-replicas cms:" + pu).read()
            if "DATASET" not in rucio_out:
                pus_to_clean.append(pu)
                config["secondaries"].pop(pu, None)
campaigns_str = json.dumps(campaigns, indent = 4)

with open("PU-clearn-report.txt", "w") as outfile:
    outfile.write("The list of PUs found:\n")
    for pu in pus: outfile.write(pu+"\n")
    outfile.write("The list of PUs removed:\n")
    for pu in pus_to_clean: outfile.write(pu+"\n")

with open("campaigns-new.json", "w") as outfile:
    outfile.write(campaigns_str)

