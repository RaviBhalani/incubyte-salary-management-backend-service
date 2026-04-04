#!/bin/bash

env=$1

docker compose -f docker-compose.$env.yaml --env-file .envs/$env/api.env down
docker compose -f docker-compose.$env.yaml --env-file .envs/$env/api.env up -d --build


