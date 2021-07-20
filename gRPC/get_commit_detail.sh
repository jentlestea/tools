#!/bin/sh

cd $INSTALL_REPO_PATH &> /dev/null

detail=`git show $1`
echo $detail

cd - &> /dev/null
