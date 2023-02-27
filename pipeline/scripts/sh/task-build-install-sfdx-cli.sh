#!/bin/bash

set -e

if [ -d ~/sfdx ]; then
    echo "$HOME/sfdx/bin" >> $GITHUB_PATH
else
    wget https://developer.salesforce.com/media/salesforce-cli/sfdx/channels/stable/sfdx-linux-x64.tar.xz
    mkdir ~/sfdx
    tar xJf sfdx-linux-x64.tar.xz -C ~/sfdx --strip-components 1
    ~/sfdx/bin/sfdx version  
    echo "$HOME/sfdx/bin" >> $GITHUB_PATH
fi

~/sfdx/bin/sfdx version 
