import setter
import io_tools
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("--config", type = str, help = "path to campaigns config json file")
parser.add_argument("--regex", type = str, help = "regex for matching pattern in campaign name")
args = parser.parse_args()

config_dict = io_tools.import_jsonfile_as_OrderedDict(args.config)
pattern = re.compile(args.regex)
for campaign in config_dict.keys():
    if pattern.search(campaign): print(campaign)

