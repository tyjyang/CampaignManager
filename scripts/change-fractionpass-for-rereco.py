import setter
import io_tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config", type = str, help = "path to campaigns config json file")
parser.add_argument("--reRecoList", type = str, help = "lapth to the Rereco campaigns json file")
parser.add_argument("--fractionPass", type = float, help = "path to campaigns config json file")
args = parser.parse_args()

config_dict = io_tools.import_jsonfile_as_OrderedDict(args.config)
rereco_campaigns = io_tools.import_jsonfile_as_OrderedDict(args.reRecoList)['ReReco_campaigns']

for campaign in config_dict.keys():
    if campaign in rereco_campaigns:
        config_dict[campaign]['fractionpass'] = args.fractionPass

io_tools.export_dict_to_jsonfile(config_dict, 'campaigns.json')


