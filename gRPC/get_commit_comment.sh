#!/bin/sh

if [ -f $WORKON_HOME/dataBase/comments/$1 ];then
	cat $WORKON_HOME/dataBase/comments/$1 > $WORKON_HOME/gRPC/.commentTmp
	echo 0
else
	echo 'No comment.' > $WORKON_HOME/gRPC/.commentTmp
	echo -1
fi
