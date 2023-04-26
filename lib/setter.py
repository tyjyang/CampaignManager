# this is a collection of function that writes to (sets up) the campaign configuration

from collections import OrderedDict

# add a PU at sites for a campaign if campaign exists in config
def add_PU_to_campaign(config_dict, PU, campaign, sites):
    if not(campaign in config_dict.keys()):
        raise ValueError("campaign %s not found in the config dictionary!" % campaign)
    if not("secondaries" in config_dict[campaign].keys()):
        config_dict[campaign]["secondaries"] = {}
    config_dict[campaign]["secondaries"][PU] = {"SiteWhitelist": sites}
