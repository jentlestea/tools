#!/bin/sh

echo "export WORKON_HOME=`pwd`" >> ~/.bashrc

mkdir -p ~/oqserver
echo "export INSTALL_REPO_PATH=~/oqserver/repo" >> ~/.bashrc
echo "export INSTALL_TARGET_BRANCH=openEuler-21.03" >> ~/.bashrc
echo "export INSTALL_SOURCE_BRANCH=Questions" >> ~/.bashrc
echo "export PYTHONPATH=`pwd`/gRPC:`pwd`/gRPC/proto" >> ~/.bashrc

if [ -z "$COMMIT_FILE_PATH" ];then
	COMMIT_DIR_PATH=~/oqserver/front
	mkdir -p $COMMIT_DIR_PATH
	COMMIT_FILE_PATH=$COMMIT_DIR_PATH/import.csv
	touch $COMMIT_FILE_PATH
fi
echo "export IMPORT_COMMIT_FILE=$COMMIT_FILE_PATH" >> ~/.bashrc

if [ -z "$REPORT_DIR_PATH" ];then
	REPORT_DIR_PATH=~/oqserver/front
	mkdir -p $REPORT_DIR_PATH
fi
echo "export OUTPUT_REPORT_DIR=$REPORT_DIR_PATH" >> ~/.bashrc

echo "alias oqserver='cd `pwd` && python3 ./gRPC/dist_server.py'" >> ~/.bashrc
source ~/.bashrc

#export PATH=$PATH:/usr/local/bin/
#python3 ./gRPC/dist_server.py > python.log 2>&1 &
