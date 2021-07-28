#!/bin/bash

commitID=$1
type=`cat $DATABASEDIR/summary/total.csv | grep $commitID | awk ' ''{print $2}'`
if [ -z "$type" ];then
	echo "UNKNOWN"
else
	echo $type
fi
