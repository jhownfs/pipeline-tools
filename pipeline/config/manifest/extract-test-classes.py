import json
import sys

test_classes = ''
i = 0 

with open(sys.argv[1]) as f:
  data = json.load(f)

for apex in data["ApexTestClass"]:
    i+=1 
    
    if(i == len(data["ApexTestClass"])):
        test_classes += apex["ApexClass"] 
    else: 
        test_classes += apex["ApexClass"] + ","
    
print(test_classes)