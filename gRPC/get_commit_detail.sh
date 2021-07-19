#!/bin/sh

cd $INSTALL_REPO_PATH
detail=`git show $1`
echo $detail
