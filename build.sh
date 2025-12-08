#!/bin/bash

pip freeze > requirements.txt

docker-compose up --build -d
