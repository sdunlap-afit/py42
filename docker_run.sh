#!/bin/bash

# Check if py42 Docker image exists
if [[ "$(docker images -q py42 2> /dev/null)" == "" ]]; then
    # Build the Docker image
    docker build -t py42 .devcontainer/
fi

docker run -it --rm -v $(pwd):/home/user/py42 -w /home/user/py42 py42 ./monte_carlo.py -n 100 -c 8

