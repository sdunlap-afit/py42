#!/bin/bash


# This script is used to deploy the py42 application to a Kubernetes cluster.
# It will be run by each instance of the container running on the cluster.
# It will:
#   1. Pull a test directory from the SMB share
#   2. Extract it
#   3. Run one or more tests
#   4. Compress the results
#   5. Push them back to the share


# TEST_DIR=$1
# INDEX=$2

# Get a random number
INDEX=$(shuf -i 1-100000 -n 1) && touch run$INDEX.txt && smbclient //pinas/shared -U pi% -c "put run$INDEX.txt"

# smbclient //pinas/shared -U pi% -c "get $TEST_DIR.tar.gz"
# smbclient //pinas/shared -U pi% -c "get monte_carlo.py"

# tar -xzf $TEST_DIR.tar.gz

# cd $TEST_DIR

# python3 monte_carlo.py -t $TEST_DIR -n 1 -c 1 -i $INDEX

# cd mc_data

# # Find the directory created with the results
# DIRNAME = $(ls -d */)

# tar -czf $DIRNAME.tar.gz $DIRNAME

# smbclient //pinas/shared -U pi% -c "put $DIRNAME.tar.gz"




