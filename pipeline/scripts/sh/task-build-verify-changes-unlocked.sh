#!/bin/bash

set -e 

sfdx force:data:soql:query -q "Select id, Commit__c from BuildLog__c order by CreatedDate DESC Limit 1" -r json -u "$USERNAME" > ./build-log-file-temp.json
SHA1_FILE=$( jq '.result.records[0].Commit__c' ./build-log-file-temp.json | tr -d '"')
echo ${SHA1_FILE}

CURRENT_SHA1=$(git rev-list HEAD | head -1)
echo ${CURRENT_SHA1}
git diff-tree --name-only ${SHA1_FILE} $CURRENT_SHA1
changedPaths=$( git diff-tree --name-only ${SHA1_FILE} $CURRENT_SHA1 )
set +e
hasChanges='false'
if [ $(echo "$changedPaths" | grep -c "^$PACKAGE_NAME") == 1 ]; then
    hasChanges='true'
fi
echo "::set-output name=hasChanges::$hasChanges
echo $hasChanges"