#!/bin/bash


# This script is used to deploy the py42 application to a Kubernetes cluster.
# It will be run by each instance of the container running on the cluster.
# It will:
#   1. Pull a test directory from the SMB share
#   2. Extract it
#   3. Run one or more tests
#   4. Compress the results
#   5. Push them back to the share

# cd to directory containing this file
cd "$(dirname "$0")"

TEST_DIR=testsc
INDEX=$JOB_COMPLETION_INDEX
echo "My index is: $INDEX"
# touch run$INDEX.txt && smbclient //10.10.10.15/shared -U pi% -c "put run$INDEX.txt"

# Get a random number
# INDEX=$(shuf -i 1-1000000 -n 1)

# INDEX=$(shuf -i 1-100000 -n 1) && touch run$INDEX.txt && smbclient //10.10.10.15/shared -U pi% -c \"put run$INDEX.txt\"

# smbclient //pinas/shared -U pi% -c "get $TEST_DIR.tar.gz"
# smbclient //pinas/shared -U pi% -c "get monte_carlo.py"

# tar -xzf $TEST_DIR.tar.gz

# cd $TEST_DIR

# multiply INDEX by 4
INDEX=$(($INDEX * 4))

python3 monte_carlo.py -t $TEST_DIR -n 4 -c 4 -i $INDEX -z

cd mc_data

# Find the directory created with the results
smbclient //10.10.10.15/shared -U pi% -c "prompt;mput *"








