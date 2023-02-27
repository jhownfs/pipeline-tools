#!/bin/bash

set -e

set +e
json=$(sfdx force:package:version:create -p $PACKAGE_NAME -c -x -w 20 -f config/project-scratch-def.json --json)
echo $json
status=$(echo $json | jq '.status')
if [ $status == "0" ]; then
    packageVersionId=$(echo $json | jq -r '.result.SubscriberPackageVersionId')
else
    echo "sfdx force:package:version:create failed"
fi

sfdx force:package:install -p $packageVersionId -w 25 -b 5 -u $USERNAME -r
sfdx force:package:version:promote -p $packageVersionId -n

exit $status
