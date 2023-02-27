#!/bin/bash

set -e

DEPLOYMENT_INFO="$(sfdx force:source:deploy --sourcepath $PATH_PACKAGE --targetusername "$USERNAME"  --testlevel $TEST_LEVEL $CHECK_ONLY_FLAG  --apiversion '54.0' --wait 0 --json)"
echo ./deployment_info.json
echo $DEPLOYMENT_INFO >> ./deployment_info.json
DEPLOYMENT_ID="$(jq -r '.result.id' ./deployment_info.json)" 
sfdx force:source:deploy:report --wait 60 -i ${DEPLOYMENT_ID} -u "$USERNAME" --verbose 
rm ./deployment_info.json
exit 0
