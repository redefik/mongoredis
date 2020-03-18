#!/bin/bash

docker rm mongo_server
docker rm redis_server
docker rm python_app
docker network remove mongo_redis_net
