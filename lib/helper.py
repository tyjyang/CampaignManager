from collections import OrderedDict
import json
import os

# change the usage of "SecondaryLocation" to "SiteWhitelist" for PU locations in a campaign dict
def change_SecondaryLocation_to_SiteWhitelist(campaigns_dict):
    for campaign, config in campaigns_dict.items():
        if "secondaries" in config.keys():
            for pu in config["secondaries"].keys():
                if "SecondaryLocation" in config["secondaries"][pu].keys():
                    campaigns_dict[campaign]["secondaries"][pu]["SiteWhitelist"] = (
                        campaigns_dict[campaign]["secondaries"][pu]["SecondaryLocation"]
                    )
                    campaigns_dict[campaign]["secondaries"][pu].pop("SecondaryLocation")
    return campaigns_dict

# get the list of sites on which the dataset is protected by a rule undre a particular rucio account 
def get_sites_with_account_rules(dataset, rucio_account):
    outstr = os.popen("rucio list-rules cms:" + dataset).read()
    rules = [x for x in outstr.split('\n') if ("STATE[OK/REPL/STUCK]" not in x and "-----" not in x and x != "")] 
    res = []
    for rule in rules:
        rule_params = rule.split()
        rule_account, rule_site = rule_params[1], rule_params[4]
        if rule_account == rucio_account:
            if "|" in rule_site:
                for x in rule_site.split("|"):
                    if x not in res: res.append(x) 
            if rule_site not in res: res.append(rule_site) 
    return res

def remove_empty_keys(dic):
    return {k: remove_empty_keys(v) if isinstance(v, dict) else v for k, v in dic.items() if v and v.keys()}

# given a config file, get a list of all PUs in that file
def get_all_PU(config_filepath, sort = True):
    campaigns = import_jsonfile_as_OrderedDict(config_filepath)
    pus = []
    for campaign, config in campaigns.items():
        for pu in config['secondaries'].keys():
            if pu not in pus: pus.append(pu)
    if sort: pus.sort()
    return pus

# given a PU, find all campaigns that are using it in a given config file
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

def get_campaigns_given_blacklisted_site(json_config, blacklisted_site, sort = True):
    campaigns_found = []
    for campaign, config in json_config.items():
        if not any([x in config.keys() for x in ['parameters', 'SiteBlacklist']]):
            continue
        elif 'SiteBlacklist' in config.keys():
            if blacklisted_site in config["SiteBlacklist"]: campaigns_found.append(campaign)
        elif 'parameters' in config.keys() and not 'SiteBlacklist' in config['parameters'].keys():
            continue
        else:
            if blacklisted_site in config['parameters']['SiteBlacklist']: campaigns_found.append(campaign)
    if sort: campaigns_found.sort()
    return campaigns_found

# given a config file, get a list of all PUs in that file
#def wmcore_get_all_PU(
