#!/bin/sh

export WORKON_HOME=`pwd`
export INSTALL_REPO_PATH=$WORKON_HOME/../repo
export INSTALL_TARGET_BRANCH=openEuler-21.03
export INSTALL_SOURCE_BRANCH=Questions
export PYTHONPATH=$WORKON_HOME/gRPC:$WORKON_HOME/gRPC/proto

python3 ./gRPC/dist_server.py
