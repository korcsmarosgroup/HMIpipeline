#!/bin/bash

docker build -t hmi:latest .
docker run -it -v "$(pwd)/output:/home/hmipipeline/output":z --rm hmi:latest /bin/bash