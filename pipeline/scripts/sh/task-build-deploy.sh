#!/bin/bash

set -e

REPOSITORY_PATH="$(git rev-parse --show-toplevel)"
TEST_ROOT_PATH="$REPOSITORY_PATH/tests"
DEFAULT_TESTS_PATH="$TEST_ROOT_PATH/default-tests"
CHECK_ONLY_FLAG=$([[ $CHECK_ONLY == "true" ]] && echo "--checkonly" || echo "")
#DESTRUCTIVE_CHANGES="./destructiveChanges/destructiveChanges.xml"
CMD_DEPLOY=("--manifest ./package/package.xml")

cd $REPOSITORY_PATH

# if [ -f "$DESTRUCTIVE_CHANGES" ]; then
#     CMD_DEPLOY+=("--predestructivechanges "$DESTRUCTIVE_CHANGES"")
#     echo ""
#     echo "destructive files found"
#     echo ""
# fi

echo "\n#### Initiate deploy in Organization #####"
echo "Running source deploy command with parameters -u "$USERNAME" --testlevel $TEST_LEVEL $CHECK_ONLY_FLAG " 

DEPLOYMENT_INFO="$(sfdx force:source:deploy ${CMD_DEPLOY[@]} --targetusername "$USERNAME"  --testlevel $TEST_LEVEL $CHECK_ONLY_FLAG --apiversion '54.0' --wait 0 --json)"
echo $DEPLOYMENT_INFO >> ./deployment_info.json
echo ./deployment_info.json
DEPLOYMENT_ID="$(jq -r '.result.id' ./deployment_info.json)" 
sfdx force:source:deploy:report --wait 60 -i ${DEPLOYMENT_ID} -u "$USERNAME" --verbose 
