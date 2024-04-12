#!/bin/bash

# Delete all containers
docker rm -f $(docker ps -a -q)

# Delete all images
docker rmi -f $(docker images -q)

# Delete all volumes
docker volume rm $(docker volume ls -q)

# Prune build cache
docker builder prune -af