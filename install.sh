#!/bin/sh

echo WORKON_HOME=`pwd` >> ~/.bashrc

mkdir -p ~/oqserver
echo INSTALL_REPO_PATH=~/oqserver/repo >> ~/.bashrc
echo INSTALL_TARGET_BRANCH=openEuler-21.03 >> ~/.bashrc
echo INSTALL_SOURCE_BRANCH=Questions >> ~/.bashrc
echo PYTHONPATH=`pwd`/gRPC:`pwd`/gRPC/proto >> ~/.bashrc

if [ -z "$COMMIT_FILE_PATH" ];then
	COMMIT_DIR_PATH=~/oqserver/front
	mkdir -p $COMMIT_DIR_PATH
	COMMIT_FILE_PATH=$COMMIT_DIR_PATH/import.csv
	touch $COMMIT_FILE_PATH
fi
echo IMPORT_COMMIT_FILE=$COMMIT_FILE_PATH >> ~/.bashrc

echo "alias oqserver=cd `pwd` && python3 ./gRPC/dist_server.py" >> ~/.bashrc

#export PATH=$PATH:/usr/local/bin/
#python3 ./gRPC/dist_server.py > python.log 2>&1 &
