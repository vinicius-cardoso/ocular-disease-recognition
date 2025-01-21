#!/bin/bash
set +e

containers=$(docker ps -q)
if [ -n "$containers" ]; then
  docker stop $containers || true
else
  echo "No containers to stop"
fi

containers=$(docker ps -aq)
if [ -n "$containers" ]; then
  docker rm -f $containers || true
else
  echo "No containers to remove"
fi

docker system prune -af
docker image prune -af
docker network prune -f

images=$(docker images -aq)
if [ -n "$images" ]; then
  docker rmi -f $images
else
  echo "No images to remove"
fi