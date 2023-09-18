from collections import OrderedDict
import json
import os

# given a PU, find all campaigns that are using it in a given config dictionary
def get_campaigns_given_PU(json_config, pu_given, sort = True):
    campaigns_found = []
    for campaign, config in json_config.items():
        if not ('secondaries' in config.keys()): continue
        for pu in config['secondaries'].keys():
            if pu == pu_given:
                campaigns_found.append(campaign)
                continue
    if sort: campaigns_found.sort()
    return campaigns_found
