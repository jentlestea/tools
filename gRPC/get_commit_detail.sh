#!/bin/sh

cd $INSTALL_REPO_PATH &> /dev/null

git show $1 > $WORKON_HOME/gRPC/.detailTmp
echo 0

cd - &> /dev/null
