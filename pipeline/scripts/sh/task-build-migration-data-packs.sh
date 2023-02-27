#!/bin/bash

set -e

DATAPACK_JOB_PATH="$REPOSITORY_PATH/Deploy.yaml"

vlocity -sfdx.username "$USERNAME" -job ${DATAPACK_JOB_PATH} packGetDiffsAndDeploy
