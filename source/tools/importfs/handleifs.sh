#!/bin/sh

file=$1

Head=`cat $file | grep 'Head' | sed -n -e 's/.*Head: \(.*\)/\1/p'`
Type=`cat $file | grep 'Type' | sed -n -e 's/.*Type: \(.*\)/\1/p'`
Description=`cat $file | grep 'Description' | sed -n -e 's/.*Description: \(.*\)/\1/p'`
Status=`cat $file | grep 'Status' | sed -n -e 's/.*Status: \(.*\)/\1/p'`

if [ -z "$Head" ] || [ -z "$Type" ] || [ -z "$Description" ];then
	echo 'invalid ifs:'$file
	exit
fi

HeadLine='['$Type']'
if [ -n "$Status" ];then
	HeadLine="$HeadLine ##$Status##"
fi
HeadLineShow="$HeadLine $Head\n"

delimO='===================================='
delimI='Body'

Body=`sed -n -e '/Body:/,//p' $file | tail +2`
BodyShow="$delimO\n$Body\n$delimO"

DescriptionShow="\nDescription: $Description\n\n"

echo -e "$HeadLineShow$DescriptionShow$BodyShow"
