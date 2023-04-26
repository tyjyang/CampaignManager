import csv
import json
from collections import OrderedDict

def import_jsonfile_as_OrderedDict(json_filepath):
    f = open(json_filepath, "r")
    return json.loads(f.read(), object_pairs_hook = OrderedDict)

def export_dict_to_jsonfile(dic, json_filepath, indent = 2, separators=(',', ': ')):
    outstr = json.dumps(dic, indent = indent, separators = separators)
    with open(json_filepath, "w") as outfile:
        outfile.write(outstr)

def get_entries_in_csv_col(csv_filepath, col_name, delimiter = ','):
    with open(csv_filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = delimiter)
        i_col_requested = 0
        res = []
        for i_row, row in enumerate(csv_reader):
            if i_row == 0:
                for i_col, col in enumerate(row):
                    if col == col_name: i_col_requested = i_col
            else:
                res.append(row[i_col_requested])
        return res
    
