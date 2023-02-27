#!/bin/bash

set -e

echo "### Get Last SHA ###"
git config --global core.quotePath false
sfdx force:data:soql:query -q "Select id, Commit__c, BranchName__c from BuildLog__c order by CreatedDate DESC Limit 1" -r json -u "$USERNAME" > ./build-log-file-temp.json
SHA1_FILE=$( jq '.result.records[0].Commit__c' ./build-log-file-temp.json | tr -d '"')
TARGET_BRANCH=$( jq '.result.records[0].BranchName__c' ./build-log-file-temp.json )
echo ${SHA1_FILE}

CURRENT_SHA1=$(git rev-list HEAD | head -1)
echo ${CURRENT_SHA1}
echo "Getting diff..."
mkdir ./pr-files

echo 'n' | sfdx sgd:source:delta --to ${CURRENT_SHA1} --from ${SHA1_FILE} --output .
chmod 777 ./destructiveChanges/destructiveChanges.xml 
git diff --name-only ${SHA1_FILE} ${CURRENT_SHA1} >> ./pr-files/diff-file
cat ./pr-files/diff-file
