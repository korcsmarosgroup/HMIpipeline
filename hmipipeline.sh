#!/bin/bash

docker build deploy/ -t hmi:latest
docker run -it --rm hmi:latest /bin/bash

