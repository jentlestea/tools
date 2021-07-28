#!/bin/bash
DATABASEDIR=$WORKON_HOME/dataBase

commitID=$1

score=`cat $DATABASEDIR/summary/total.csv | grep $commitID | awk ' ''{print $4}'`

if [ -z "$score" ];then
	echo '?'
else
	echo $score
fi
