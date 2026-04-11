#!/bin/bash

env=$1

if [ "$env" = "local" ]; then
    env_file=".envs/local.env"
else
    env_file=".envs/$env/api.env"
fi

docker compose -f docker-compose.$env.yaml --env-file "$env_file" down
docker compose -f docker-compose.$env.yaml --env-file "$env_file" up -d --build