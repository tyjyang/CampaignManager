import helper
import setter
import io_tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", type = str, help = "path to json config file")
parser.add_argument("--fraction", type = float, help = "fraction for partial copy, set for all campaigns")
parser.add_argument("--omit", type = str, nargs = "*", help = "partial copy settings won't be changed for those campaigns")

args = parser.parse_args()

campaigns = io_tools.import_jsonfile_as_OrderedDict(args.input)

if not args.omit: args.omit = []
for camp in campaigns:
    if (
        camp not in args.omit and 
        "partial_copy" in campaigns[camp].keys() and
        campaigns[camp]["partial_copy"] > args.fraction
    ):
        campaigns[camp]["partial_copy"] = args.fraction
io_tools.export_dict_to_jsonfile(campaigns, 'campaigns_new.json')

