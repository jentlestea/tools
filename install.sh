#!/bin/sh

export WORKON_HOME=`pwd`
export PYTHONPATH=$WORKON_HOME/gRPC:$WORKON_HOME/gRPC/proto

python3 ./gRPC/dist_server.py
