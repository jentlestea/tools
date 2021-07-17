#!/bin/sh

sed -i '' '/WORKON_HOME=/d' ~/.bashrc

sed -i '' '/INSTALL_REPO_PATH=/d' ~/.bashrc
sed -i '' '/INSTALL_TARGET_BRANCH=/d' ~/.bashrc
sed -i '' '/INSTALL_SOURCE_BRANCH=/d' ~/.bashrc
sed -i '' '/PYTHONPATH=/d' ~/.bashrc
sed -i '' '/IMPORT_COMMIT_FILE=/d' ~/.bashrc
sed -i '' '/alias oqserver=/d' ~/.bashrc
sed -i '' '/OUTPUT_REPORT_DIR=/d' ~/.bashrc
