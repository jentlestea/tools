#!/bin/sh

CONFPATH=/etc/profile.d/qs.sh

if [ -f $CONFPATH ];then
	exit
fi

if [ $# != 1 ];then
	exit
fi
TARGETDIR=$1

echo "export WORKON_HOME=$TARGETDIR" >> $CONFPATH

mkdir -p ~/oqserver
echo "export INSTALL_REPO_PATH=~/oqserver/repo" >> $CONFPATH
echo "export INSTALL_TARGET_BRANCH=openEuler-21.03" >> $CONFPATH
echo "export INSTALL_SOURCE_BRANCH=Questions" >> $CONFPATH
echo "export SPYTHONPATH=$TARGETDIR/gRPC:$TARGETDIR/gRPC/proto" >> $CONFPATH
mkdir -p ~/oqserver/pool/ifs
echo "export IFSPATH=~/oqserver/pool/ifs" >> $CONFPATH
if [ -z "$COMMIT_FILE_PATH" ];then
	COMMIT_DIR_PATH=~/oqserver/front
	mkdir -p $COMMIT_DIR_PATH
	COMMIT_FILE_PATH=$COMMIT_DIR_PATH/import.csv
	touch $COMMIT_FILE_PATH
fi
echo "export IMPORT_COMMIT_FILE=$COMMIT_FILE_PATH" >> $CONFPATH
if [ -z "$REPORT_DIR_PATH" ];then
	REPORT_DIR_PATH=~/oqserver/front
	mkdir -p $REPORT_DIR_PATH
fi
echo "export OUTPUT_REPORT_DIR=$REPORT_DIR_PATH" >> $CONFPATH
echo "alias oqserver='cd $TARGETDIR && python3 ./gRPC/dist_server.py'" >> $CONFPATH
echo "alias oqserver-tool='python3 $TARGETDIR/tools/oqserver-tool.py'" >> $CONFPATH
