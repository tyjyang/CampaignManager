from lib import setter, getter, io_tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config", type = str, help = "path to campaigns config json file")
parser.add_argument("--PU", type = str, help = "name of the pileup sample to set sitewhitelist for")
parser.add_argument("--sites",  type = str, nargs = "*", help = "site whitelist for the pileup")
args = parser.parse_args()

config_dict = io_tools.import_jsonfile_as_OrderedDict(args.config)
campaigns = getter.get_campaigns_given_PU(config_dict, args.PU)

for campaign in campaigns:
    config_dict[campaign]['secondaries'][args.PU]['SiteWhitelist'] = args.sites

io_tools.export_dict_to_jsonfile(config_dict, 'campaigns.json')
