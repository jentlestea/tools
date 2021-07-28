#!/bin/sh

file=$1
log=$2

VerifyCode=`cat $file | grep 'VerifyCode' | sed -n -e 's/.*VerifyCode: \(.*\)/\1/p'`
cd $INSTALL_REPO_PATH
git checkout $INSTALL_SOURCE_BRANCH &> /dev/null
found=`git log | grep "VerifyCode: $VerifyCode"`
if [[ -n "$VerifyCode" ]] && [[ -n $found ]];then
	echo 0
	exit
fi
cd - &>/dev/null

if [ -z "$VerifyCode" ];then
	VerifyCode=`echo $(($(date +%s%N)/1000000))`
	sed -i -e "1i VerifyCode: $VerifyCode" $file
fi

ReportedBy=`cat $file | grep 'Reported-by' | sed -n -e 's/.*Reported-by: \(.*\)/\1/p'`
Head=`cat $file | grep 'Head' | sed -n -e 's/.*Head: \(.*\)/\1/p'`
Type=`cat $file | grep 'Type' | sed -n -e 's/.*Type: \(.*\)/\1/p'`
Description=`cat $file | grep 'Description' | sed -n -e 's/.*Description: \(.*\)/\1/p'`
Status=`cat $file | grep 'Status' | sed -n -e 's/.*Status: \(.*\)/\1/p'`

if [ -z "$Head" ] || [ -z "$Type" ] || [ -z "$Description" ];then
	echo '[ERROR] invalid ifs:'$file >> $log
	echo 0
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

ReportedByShow="Reported-by: $ReportedBy"
DescriptionShow="Description: $Description"
VerifyCodeShow="VerifyCode: $VerifyCode"
cd $INSTALL_REPO_PATH
git checkout $INSTALL_SOURCE_BRANCH &> /dev/null
git commit -m "$HeadLineShow" -m "$VerifyCodeShow" -m "$ReportedByShow" -m "$DescriptionShow" -m "$delimO" -m "$BodyShow" -m "$delimO" --allow-empty &> /dev/null
commitID=`git log --oneline -1 | awk ' ''{print $1}'`

cd - &>/dev/null
echo $commitID
