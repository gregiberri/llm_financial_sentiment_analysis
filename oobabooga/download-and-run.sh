#!/bin/bash
echo "Downloading $1"
#python ./download-model.py $1 --threads 16 --output /models/
echo "Starting server with model $1 and loader $2"
python server.py  --listen --listen-host 0.0.0.0 --listen-port 7860 --extensions api --model-dir /models --share
# --model ${1/\//"_"} --loader $2
