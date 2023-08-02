import argparse
import io_tools
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--campConfig", type = str, help = "json file for campaign configuration")
parser.add_argument("--sitesToAdd", type = str, nargs = "*", help = "sites to add to the el8 blacklist")
parser.add_argument("--sitesToRemove", type = str, nargs = "*", help = "sites to remove from the el8 blacklist")

args = parser.parse_args()

el8bl_old = io_tools.import_jsonfile_as_OrderedDict("inputs/el8-blacklist.json")['el8-blacklist']
campaigns = io_tools.import_jsonfile_as_OrderedDict(args.campConfig)

el8bl = el8bl_old.copy()
if args.sitesToAdd:
    for site_add in args.sitesToAdd: el8bl.append(site_add)
if args.sitesToRemove:
    for site_remove in args.sitesToRemove: el8bl.remove(site_remove)

for campaign, config in campaigns.items():
    if 'SiteBlacklist' in config.keys():
        if all([x in config['SiteBlacklist'] for x in el8bl_old]):
            if args.sitesToAdd:
                for site_add in args.sitesToAdd: config['SiteBlacklist'].append(site_add)
            if args.sitesToRemove:
                for site_remove in args.sitesToRemove: config['SiteBlacklist'].remove(site_remove)

campaigns_new = json.dumps(campaigns, indent = 2, separators=(',', ': '))
el8_dict = {'el8-blacklist': el8bl}
el8bl_new = json.dumps(el8_dict, indent = 2, separators=(',', ': '))

with open("inputs/el8-blacklist.json", "w") as out:
    out.write(el8bl_new)
with open("campaigns-new.json", "w") as out:
    out.write(campaigns_new)
