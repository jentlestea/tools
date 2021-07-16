#!/bin/bash
DATABASEDIR=$WORKON_HOME/dataBase

commitID=$1

score=`cat $DATABASEDIR/summary/total.csv | grep $commitID | awk ' ''{print $3}`

if [ -n "$score" ];then
	echo '?'
elif
	echo $score
fi
