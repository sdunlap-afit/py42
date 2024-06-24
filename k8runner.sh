#!/bin/bash

# This script is used to deploy run monte carlo simulations in a Kubernetes cluster.
# It will be run by each instance of the container running on the cluster.
# It will:
#   1. Run one or more tests
#   2. Compress the results
#   3. Push them back to the share

# This script is currently added directly to the docker 
# image during a build, and it expects the rest of the py42 files
# to be present in the same directory.
# We could change this behavior to have the script download the
# py42 directory from the share, but that will add more overhead.
# It might be a good idea to do if we upgrade to bigger servers
# that can run many sims in one image.

# cd to directory containing this file
cd "$(dirname "$0")"

TEST_DIR=testsc
INDEX=$JOB_COMPLETION_INDEX
# echo "My index is: $INDEX"

# Only do this if each instance is running 4 sims at a time

# multiply INDEX by 4
# INDEX=$(($INDEX * 4))
# python3 monte_carlo.py -t $TEST_DIR -n 4 -c 4 -i $INDEX -z

# Run one test and compress the results
python3 monte_carlo.py -t $TEST_DIR -n 1 -c 1 -i $INDEX -z

cd mc_data

# Upload all of the compressed results to the share
smbclient //10.10.10.15/shared -U pi% -c "prompt;mput *"


