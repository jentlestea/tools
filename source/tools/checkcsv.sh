#!/bin/sh

file=$1

if [ ! -f $file ];then
	echo -1
fi
cat $file | while read line
do
	commitID=`echo $line | awk ' ''{print $1}'`
	type=`echo $line | awk ' ''{print $2}'`
	bugzilla=`echo $line | awk ' ''{print $3}'`
	score=`echo $line | awk ' ''{print $4}'`
	if [[ $commitID == '' ]] || [[ $type == '' ]] || [[ $bugzilla == '' ]] || [[ $score == '' ]];then
		echo 0
		exit
	fi
done
echo 0
