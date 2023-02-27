#!/bin/bash

set -e 

echo '{
    "records":[
        {
            "attributes":{
                "type": "DeploymentInformation__c",
                "referenceId": "BuildLogRef1"
            },
        "BranchName__c": "",
        "Commit__c": "",
        "DeploymentDate__c": "",
        "Author__c": ""
        }
    ]
}' > ./build-log-file-temp.json

LAST_VERSION_SHA=$(git rev-list HEAD | head -1)

echo $LAST_VERSION_SHA
echo $GITHUB_BASE_REF
echo $GITHUB_REF_NAME
echo $GITHUB_ACTOR


jq --arg BRANCH_NAME $GITHUB_REF_NAME  \
                               --arg COMMIT_SHA $LAST_VERSION_SHA \
                               --arg AUTHOR_NAME "$GITHUB_ACTOR"  \
                               '.records[0] |= ( .BranchName__c = $BRANCH_NAME | .Commit__c = $COMMIT_SHA  | .Author__c = $AUTHOR_NAME )' ./build-log-file-temp.json > ./build-log-file.json

sfdx force:data:tree:import -f ./build-log-file.json -u  "$USERNAME"


