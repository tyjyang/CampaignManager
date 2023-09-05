import helper
import setter
import io_tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--oldConfig", type = str, help = "filepath to old campaigns config as the baseline of restoration")
parser.add_argument("--newConfig", type = str, help = "filepath to new campaigns config on which the restoration is applied")
parser.add_argument("--PUCsv", type = str, help = "input csv file for PUs")

parser.add_argument("--delimiter", type = str, default = ",", help = "delimiter used in the csv")
parser.add_argument("--colName", type = str, default = "NAME", help = "column name for PUs in csv")
args = parser.parse_args()

PUs = io_tools.get_entries_in_csv_col(args.PUCsv, args.colName, args.delimiter)

old_json_obj = io_tools.import_jsonfile_as_OrderedDict(args.oldConfig)
new_json_obj = io_tools.import_jsonfile_as_OrderedDict(args.newConfig)

sites = ["T1_US_FNAL_Disk", "T2_CH_CERN"]
for pu in PUs:
    print(pu)
    campaigns_for_pu = helper.get_campaigns_given_PU(old_json_obj, pu, sort = False)
    for campaign in campaigns_for_pu:
        print(campaign)
        setter.add_PU_to_campaign(new_json_obj, pu, campaign, sites)
        setter.set_PU_attr(new_json_obj, pu, "keepOnDisk", True)
        setter.set_PU_attr(new_json_obj, pu, "fractionOnDisk", 1.0)

io_tools.export_dict_to_jsonfile(new_json_obj, 'campaigns_new.json')

