import json
import os
from collections import OrderedDict

f = open("../WmAgentScripts/campaigns.json", "r")
campaigns = json.loads(f.read(), object_pairs_hook=OrderedDict)

# get the list of sites on which the dataset is protected by a rule undre a particular rucio account 
def get_sites_with_account_rules(dataset, rucio_account):
    outstr = os.popen("rucio list-rules cms:" + dataset).read()
    rules = [x for x in outstr.split('\n') if ("ID" not in x and "-----" not in x and x != "")] 
    res = []
    for rule in rules:
        rule_params = rule.split()
        rule_account, rule_site = rule_params[1], rule_params[4]
        if rule_account == rucio_account:
            if "|" in rule_site:
                for x in rule_site.split("|"):
                    print(dataset)
                    res.append(x)
            res.append(rule_site)
    return res

with open("log_cleanup.txt", "w") as log:
    i = 0
    pus = []
    pus_to_clean = []
    for campaign, config in campaigns.items():
        if "secondaries" in config.keys():
            for pu in config["secondaries"].keys():
                if pu not in pus: pus.append(pu)
                pu_sites_wmcore = get_sites_with_account_rules(pu, "wmcore_transferor")
                if len(pu_sites_wmcore) == 0:
                    campaigns[campaign]["secondaries"].pop(pu)
                    i += 1
                    log.write(str(i) + ". ++++++++++++++++++++++++++++++++++++++++++++++\n")
                    log.write("removed PU " + pu + " in campaign " + campaign + " due to no rules under wmcore_transferor.")
                    log.write("\n")
                    continue
                if "SiteWhitelist" in config["secondaries"][pu]: pu_sites_config = config["secondaries"][pu]["SiteWhitelist"]
                else: pu_sites_config = []
                if any([x not in pu_sites_wmcore for x in pu_sites_config]):
                    config["secondaries"][pu]["SiteWhitelist"] = pu_sites_wmcore
                    i += 1
                    log.write(str(i) + ". ++++++++++++++++++++++++++++++++++++++++++++++\n")
                    log.write("changed site whitelist for " + pu + " from:\n")
                    for x in pu_sites_config: log.write(x + ' ')
                    log.write("\n")
                    log.write("to:\n")
                    for x in pu_sites_wmcore: log.write(x + ' ')
                    log.write("\n")

    campaigns_str = json.dumps(campaigns, indent = 2, separators=(',', ': '))

    
with open("campaigns-new.json", "w") as outfile:
    outfile.write(campaigns_str)

