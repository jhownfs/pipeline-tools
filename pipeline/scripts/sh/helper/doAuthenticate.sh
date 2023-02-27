#!/bin/bash

set -e 

echo "$PRIVATE_KEY"  > server.key
echo "#### Step to Authenticate in Organization #####"
sfdx force:auth:jwt:grant --setdefaultdevhubusername -i $CLIENT_ID -f ./server.key -u $USERNAME  -r $INSTANCE_URL 
 