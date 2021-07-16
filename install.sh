#!/bin/sh

export WORKON_HOME=`pwd`
export INSTALL_REPO_PATH=$WORKON_HOME/../repo
export INSTALL_TARGET_BRANCH=openEuler-21.03
export INSTALL_SOURCE_BRANCH=Questions
export PYTHONPATH=$WORKON_HOME/gRPC:$WORKON_HOME/gRPC/proto

if [ -z "$COMMIT_FILE_PATH" ];then
	COMMIT_DIR_PATH=~/Qimport
	mkdir -p $COMMIT_DIR_PATH
	COMMIT_FILE_PATH=$COMMIT_DIR_PATH/import.csv
	touch $COMMIT_FILE_PATH
fi
export IMPORT_COMMIT_FILE=$COMMIT_FILE_PATH

python3 ./gRPC/dist_server.py
