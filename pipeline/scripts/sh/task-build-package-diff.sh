#!/bin/bash

set -e

SFDX_API_VERSION=54.0 
REPOSITORY_PATH="$(git rev-parse --show-toplevel)"
SCRIPTS_PATH="$REPOSITORY_PATH/scripts"
HELPER_SCRIPTS_PATH="$SCRIPTS_PATH/sh/helper"
TEST_ROOT_PATH="$REPOSITORY_PATH/tests"
DEFAULT_TESTS_PATH="$TEST_ROOT_PATH/default-tests"
CHECK_ONLY_FLAG=$([[ $CHECK_ONLY == "true" ]] && echo "--checkonly" || echo "")
DESTRUCTIVE_CHANGES="../destructiveChanges/destructiveChanges.xml"

echo "\n#### Building Package to Deploy #####"
python --version
sfdx force:project:create --projectname $PROJECT_NAME --template empty
python $PATH_PIPELINE_TOOLS/config/copy-files-beta.py ./ ./pr-files/diff-file $PROJECT_NAME

cd $PROJECT_NAME

echo "\n#### Initiate deploy in Organization #####"
echo "Running source deploy command with parameters -u "$USERNAME" --testlevel $TEST_LEVEL $CHECK_ONLY_FLAG " 
ls 

DEPLOYMENT_INFO="$(sfdx force:source:deploy --sourcepath ./force-app/main --targetusername "$USERNAME"  --testlevel $TEST_LEVEL $CHECK_ONLY_FLAG  --apiversion '54.0'  --wait 0 --json)"
echo $DEPLOYMENT_INFO >> ./deployment_info.json
echo ./deployment_info.json
DEPLOYMENT_ID="$(jq -r '.result.id' ./deployment_info.json)" 
sfdx force:source:deploy:report --wait 60 -i ${DEPLOYMENT_ID} -u "$USERNAME" --verbose 

exit 0
