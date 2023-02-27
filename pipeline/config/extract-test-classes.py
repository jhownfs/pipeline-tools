import os
import json
import sys
test_classes = ""
key_to_lookup = "ApexTestClass"
path_to_json = "./tests"

def processFile(ffile):
    result = ""
    with open(ffile) as f:
        data = json.load(f)
        if key_to_lookup in data:
            result += ", ".join(data[key_to_lookup])
    return result

if len(sys.argv) > 1:
    path_to_json = sys.argv[1]

if os.path.isdir(path_to_json) or os.path.isfile(path_to_json):
    if os.path.isfile(path_to_json):
        test_classes = processFile(path_to_json)
    else:
        json_files = [pos_json for pos_json in os.listdir(
            path_to_json) if pos_json.endswith('.json')]
        for json_file in json_files:
            json_file = path_to_json + '/' + json_file
            test_classes += processFile(json_file) + ", "
        test_classes = test_classes[:-2]
    if len(test_classes) > 0:
        # TODO does not repeat item to test
        #test_classes = ','.join(map(str, test_classes.split(',')))
        print(test_classes)