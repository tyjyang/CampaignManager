import helper
import json
import os
from collections import OrderedDict

campaigns = io_tools.import_jsonfile_as_OrderedDict("tests/test-campaigns.json")
campaigns = helper.change_SecondaryLocation_to_SiteWhitelist(campaigns)

with open("log_cleanup.txt", "w") as log:
    i = 0
    pus = []
    pus_to_clean = []
    for campaign, config in campaigns.items():
        if "secondaries" in config.keys():
            for pu in config["secondaries"].keys():
                if pu not in pus: pus.append(pu)
                pu_sites_wmcore = helper.get_sites_with_account_rules(pu, "wmcore_transferor")
                if len(pu_sites_wmcore) == 0:
                    campaigns[campaign]["secondaries"].pop(pu)
                    i += 1
                    log.write(str(i) + ". ++++++++++++++++++++++++++++++++++++++++++++++\n")
                    log.write("removed PU " + pu + " in campaign " + campaign + " due to no rules under wmcore_transferor.")
                    log.write("\n")
                    continue
                if "SiteWhitelist" in config["secondaries"][pu]:
                    pu_sites_config = config["secondaries"][pu]["SiteWhitelist"]
                elif "SecondaryLocation" in config["secondaries"][pu]:
                    pu_sites_config = config["secondaries"][pu]["SecondaryLocation"]
                else: pu_sites_config = []
                if any([x not in pu_sites_wmcore for x in pu_sites_config]):
                    config["secondaries"][pu]["SiteWhitelist"] = pu_sites_wmcore
                    i += 1
                    log.write(str(i) + ". ++++++++++++++++++++++++++++++++++++++++++++++\n")
                    log.write("changed site whitelist for " + pu + " in campaign " + campaign + " from:\n")
                    for x in pu_sites_config: log.write(x + ' ')
                    log.write("\n")
                    log.write("to:\n")
                    for x in pu_sites_wmcore: log.write(x + ' ')
                    log.write("\n")

    campaigns_str = json.dumps(campaigns, indent = 2, separators=(',', ': '))

    
with open("campaigns-new.json", "w") as outfile:
    outfile.write(campaigns_str)

