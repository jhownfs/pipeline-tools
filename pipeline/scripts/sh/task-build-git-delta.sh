#!/bin/bash

set -e

echo 'y' | ~/sfdx/bin/sfdx plugins:install sfdx-git-delta
echo 'y' | ~/sfdx/bin/sfdx plugins:install @salesforce/sfdx-scanner



REPOSITORY_PATH="$(git rev-parse --show-toplevel)"
SOURCE_PATH='./force-app'
CODE_SCAN_PATH='../code-scan'
CODE_SCAN_RESULTS_DIR='../scan-result'
CODE_SCAN_RESULTS="${CODE_SCAN_RESULTS_DIR}/apexScanResults.sarif"
CODE_SCAN_RULE='../pipeline/config/pmd/apex_ruleset.xml'
DIR_DIFF='../diff'
echo "### Get Last SHA ###"
git config --global core.quotePath false
sfdx force:data:soql:query -q "Select id, Commit__c, BranchName__c from DeploymentInformation__c order by CreatedDate DESC Limit 1" -r json -u "$USERNAME" > ./build-log-file-temp.json
SHA1_FILE=$( jq '.result.records[0].Commit__c' ./build-log-file-temp.json | tr -d '"')
TARGET_BRANCH=$( jq '.result.records[0].BranchName__c' ./build-log-file-temp.json )
echo "Last Build SHA1 on Org "${SHA1_FILE}""

CURRENT_SHA1=$(git rev-list HEAD | head -1)
echo "Current SHA1 "${CURRENT_SHA1}""

echo ""
echo "Getting diff..."
echo ""

cd $REPOSITORY_PATH
sfdx sgd:source:delta -s ${SOURCE_PATH} --to ${CURRENT_SHA1} --from ${SHA1_FILE} --output .

# DESTRUCTIVE_CHANGES="$(git diff --name-only --diff-filter=D ${SHA1_FILE} ${CURRENT_SHA1})"
# if [ -n "$DESTRUCTIVE_CHANGES" ]; then
#     echo ""
#     echo "destructive files found"
#     echo ""
#     echo "$DESTRUCTIVE_CHANGES"
# else
#     rm -rf ./destructiveChanges
# fi

CHANGES="$(git diff --name-only --diff-filter=d ${SHA1_FILE} ${CURRENT_SHA1})"
if [ -n "$CHANGES" ]; then
    echo ""
    echo "metadata to build"
    echo ""
    echo "$CHANGES"

    mkdir "$DIR_DIFF"
    git diff --name-only --diff-filter=d "$SHA1_FILE" "$CURRENT_SHA1" | xargs -E -0 -I {} cp {} "$DIR_DIFF"
    
    mkdir "$CODE_SCAN_PATH"
    mkdir "$CODE_SCAN_RESULTS_DIR"

    #find $(cat "$FILE_DIFF") -name "force-app/main/default/classes/*.cls" -exec cp -- "{}" "$CODE_SCAN_PATH" \;

    find "$DIR_DIFF" -name "*.cls" -exec cp -- "{}" "$CODE_SCAN_PATH" \;

    echo ""
    echo ""
    echo "#### Running Code Scan #####"
    echo ""

    #sfdx scanner:run --format sarif --target "$CODE_SCAN_PATH" --pmdconfig="$CODE_SCAN_RULE" --outfile "$CODE_SCAN_RESULTS"
fi
