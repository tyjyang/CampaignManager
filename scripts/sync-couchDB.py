import argparse
import io_tools
import os

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--campConfig", type = str, help = "json file for campaign configuration")
parser.add_argument("-a", "--campsToAdd", type = str, nargs = "*", help = "new campaigns added to the config")
parser.add_argument("--dirWmAgentScripts", type = str, default = "/data/unifiedPy3-fast/WmAgentScripts", help = "path to the WmAgentScripts repo")

args = parser.parse_args()

campaigns_config = io_tools.import_jsonfile_as_OrderedDict(args.campConfig)

for camp in args.campsToAdd:
    camp_config = dict(campaigns_config[camp])
    os.system(f"python3 {args.dirWmAgentScripts}/campaignsConfiguration.py --name {camp} --configuration {camp_config}")

