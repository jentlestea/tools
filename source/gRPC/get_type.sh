#!/bin/bash

SOURCE_BRANCH=$INSTALL_SOURCE_BRANCH
REPOPATH=$INSTALL_REPO_PATH
DATABASEDIR=$WORKON_HOME/dataBase

commitID=$1

cd $REPOPATH &> /dev/null
commitMsg=`git show --format=%B $commitID $SOURCE_BRANCH  | head -n 1`
bug=`echo $commitMsg | grep '##BUG##'`
course=`echo $commitMsg | grep '##COURSE##'`

if [ -n "$bug" ]; then
	echo 'BUG'
elif [ -n "$course" ]; then
	echo 'COURSE'
else
	rejected=`cat $DATABASEDIR/mergeConflicts | grep $commitID`
	if [ -z "$rejected" ];then
		echo 'LTS'
	else
		echo 'LTS[C]'
	fi
fi
cd - &> /dev/null
