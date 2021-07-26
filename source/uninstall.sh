#!/bin/sh

if [[ `uname` == 'Darwin' ]];then
	sed -i '' '/WORKON_HOME=/d' ~/.bashrc
	sed -i '' '/INSTALL_REPO_PATH=/d' ~/.bashrc
	sed -i '' '/INSTALL_TARGET_BRANCH=/d' ~/.bashrc
	sed -i '' '/INSTALL_SOURCE_BRANCH=/d' ~/.bashrc
	sed -i '' '/SPYTHONPATH=/d' ~/.bashrc
	sed -i '' '/IMPORT_COMMIT_FILE=/d' ~/.bashrc
	sed -i '' '/alias oqserver=/d' ~/.bashrc
	sed -i '' '/OUTPUT_REPORT_DIR=/d' ~/.bashrc
else
	sed -i '/WORKON_HOME=/d' ~/.bashrc
	sed -i '/INSTALL_REPO_PATH=/d' ~/.bashrc
	sed -i '/INSTALL_TARGET_BRANCH=/d' ~/.bashrc
	sed -i '/INSTALL_SOURCE_BRANCH=/d' ~/.bashrc
	sed -i '/SPYTHONPATH=/d' ~/.bashrc
	sed -i '/IMPORT_COMMIT_FILE=/d' ~/.bashrc
	sed -i '/alias oqserver=/d' ~/.bashrc
	sed -i '/OUTPUT_REPORT_DIR=/d' ~/.bashrc
fi
source ~/.bashrc
