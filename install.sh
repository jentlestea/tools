#!/bin/sh

export WORKON_HOME=`pwd`
export INSTALL_REPO_PATH=$WORKON_HOME/../repo

export INSTALL_TARGET_BRANCH=openEuler-21.03
export INSTALL_SOURCE_BRANCH=Questions
export PYTHONPATH=$WORKON_HOME/gRPC:$WORKON_HOME/gRPC/proto

#CHECK REPO
if [ ! -d $INSTALL_REPO_PATH ];then
	echo 'ERROR: '$INSTALL_REPO_PATH' not exit.'
	return
fi

cd $INSTALL_REPO_PATH
if [ ! `git branch | grep $INSTALL_TARGET_BRANCH` ];then
	echo 'ERROR: branch '$INSTALL_TARGET_BRANCH' not exit.'
	return
fi
if [ ! `git branch | grep $INSTALL_SOURCE_BRANCH` ];then
	echo 'ERROR: branch '$INSTALL_SOURCE_BRANCH' not exit.'
	return
fi
cd - 2>&1 >/dev/null

if [ -z "$COMMIT_FILE_PATH" ];then
	COMMIT_DIR_PATH=~/QI
	mkdir -p $COMMIT_DIR_PATH
	COMMIT_FILE_PATH=$COMMIT_DIR_PATH/import.csv
	touch $COMMIT_FILE_PATH
fi
export IMPORT_COMMIT_FILE=$COMMIT_FILE_PATH

python3 ./gRPC/dist_server.py
return
