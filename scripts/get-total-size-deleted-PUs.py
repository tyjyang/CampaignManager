import datasets
import io_tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type = str, help = "input csv file for PUs")
parser.add_argument("--colName", type = str, default = "NAME", help = "column name for PUs in csv")
parser.add_argument("--delimiter", type = str, default = ",", help = "delimiter used in the csv")
args = parser.parse_args()

PUs = io_tools.get_entries_in_csv_col(args.input, args.colName, args.delimiter)
size = 0
for pu in PUs:
    size += datasets.get_size_of_dataset(pu)
print("total size is: %d TB" % (size / 1e12))
