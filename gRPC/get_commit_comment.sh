#!/bin/sh

if [ -f $WORKON_HOME/dataBase/comments/$1 ];then
	comment=`cat $WORKON_HOME/dataBase/comments/$1`
else
	comment='No comment.'
fi

echo $comment
