import helper
import setter
import io_tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", type = str, help = "path to json config file")
parser.add_argument("--disable", type = str, nargs = "*", help = "campaigns to be disabled")

args = parser.parse_args()

campaigns = io_tools.import_jsonfile_as_OrderedDict(args.input)

for camp in campaigns.keys():
    if camp in args.disable:
        campaigns[camp]["go"] = False
        if "secondaries" in campaigns[camp].keys():
            for PU in campaigns[camp]["secondaries"].keys():
                if "keepOnDisk" in campaigns[camp]["secondaries"][PU].keys():
                    campaigns[camp]["secondaries"][PU]["keepOnDisk"] = False
io_tools.export_dict_to_jsonfile(campaigns, 'campaigns_new.json')

