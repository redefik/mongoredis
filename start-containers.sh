#!/bin/bash

# Create a docker network for abilitating communications between containers
docker network create mongo_redis_net

# Launch a mongo_server container listening on port 27017 attached to
# mongo_redis_net network
docker run -i -t -d -p 27017:27017 --name mongo_server --network=mongo_redis_net mongo:latest /usr/bin/mongod --bind_ip_all

# Launch a redis_server container listening on port 6379 attached to
# mongo_redis_net network
docker run -i -t -d -p 6379:6379 --name redis_server --network=mongo_redis_net sickp/alpine-redis

# Launch a container executing the Python web service listening on 0.0.0.0:80
# The container is attached to the mongo_redis_net network
docker run -i -t -p 80:80 --name python_app --network=mongo_redis_net my_mongo_redis
