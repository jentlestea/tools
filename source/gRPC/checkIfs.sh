#!/bin/sh

file=$1

Head=`cat $file | grep 'Head' | sed -n -e 's/.*Head: \(.*\)/\1/p'`
Type=`cat $file | grep 'Type' | sed -n -e 's/.*Type: \(.*\)/\1/p'`
Body=`cat $file | grep 'Body' | sed -n -e 's/.*Body: \(.*\)/\1/p'`
Description=`cat $file | grep 'Description' | sed -n -e 's/.*Description: \(.*\)/\1/p'`
if [[ -z "$Head" ]] || [[ -z "$Type" ]] || [[ -z "$Body" ]] || [[ -z "$Description" ]];then
	rm -f $file
	echo '-1'
	exit
fi
echo '0'
