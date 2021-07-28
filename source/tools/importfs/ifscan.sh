#!/bin/sh

TOOLSCRIPTDIR=$WORKON_HOME/tools/importfs

dir=$IFSPATH
if [ -z "$dir" ];then
	echo -1
	exit
fi

cat /dev/null > ./import.csv.tmp

for file in `ls $dir`
do
	commitID=`bash -x $TOOLSCRIPTDIR/handleifs.sh $file`
	if [ -n "$commitID" ];then
		echo $commitID >> ./import.csv.tmp
	fi
done
echo 0
