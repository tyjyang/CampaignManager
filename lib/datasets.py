import os
import json
from collections import OrderedDict
import helper

def get_size_of_dataset(dataset):
    query_cmd = 'dasgoclient -query="dataset=%s" -json' % dataset
    json_obj = json.loads(os.popen(query_cmd).read(), object_pairs_hook = OrderedDict)
    if not json_obj:
        raise ValueError('dasgoclient request for %s went wrong' % dataset)
    for das_dict in json_obj:
        if 'dbs3:filesummaries' in das_dict['das']['services']:
            for dataset_dict in das_dict['dataset']:
                if "size" in dataset_dict.keys():
                    print("size of dataset %s is %d TB" % (dataset, dataset_dict["size"]/1e12))
                    return dataset_dict["size"]

