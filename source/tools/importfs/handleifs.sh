#!/bin/sh

file=$1
log=$2

VerifyCode=`cat $file | grep 'VerifyCode' | sed -n -e 's/.*VerifyCode: \(.*\)/\1/p'`
cd $INSTALL_REPO_PATH
git checkout $INSTALL_SOURCE_BRANCH
found=`git log | grep "VerifyCode: $VerifyCode"`
if [[ -n "$VerifyCode" ]] && [[ -n $found ]];then
	#echo 0
	exit
fi
cd - 2>&1 >/dev/null

if [ -z "$VerifyCode" ];then
	VerifyCode=`echo $(($(date +%s%N)/1000000))`
	sed -i -e "1i VerifyCode: $VerifyCode" $file
fi

Head=`cat $file | grep 'Head' | sed -n -e 's/.*Head: \(.*\)/\1/p'`
Type=`cat $file | grep 'Type' | sed -n -e 's/.*Type: \(.*\)/\1/p'`
Description=`cat $file | grep 'Description' | sed -n -e 's/.*Description: \(.*\)/\1/p'`
Status=`cat $file | grep 'Status' | sed -n -e 's/.*Status: \(.*\)/\1/p'`

if [ -z "$Head" ] || [ -z "$Type" ] || [ -z "$Description" ];then
	echo '[ERROR] invalid ifs:'$file >> $log
	#echo 0
	exit
fi

HeadLine='['$Type']'
if [ -n "$Status" ];then
	HeadLine="$HeadLine ##$Status##"
fi
HeadLineShow="$HeadLine $Head"

delimO='===================================='
delimI='Body'

Body=`sed -n -e '/Body:/,//p' $file | tail +2`
BodyShow="$Body"

DescriptionShow="Description: $Description"
VerifyCodeShow="VerifyCode: $VerifyCode"

cd $INSTALL_REPO_PATH
git checkout $INSTALL_SOURCE_BRANCH
git commit -m "$HeadLineShow" -m "$VerifyCodeShow" -m "$DescriptionShow" -m "$delimO" -m "$BodyShow" -m "$delimO" --allow-empty
commitID=`git log --oneline -1 | awk ' ''{print $1}'`
cd - 2>&1 >/dev/null
echo $commitID
