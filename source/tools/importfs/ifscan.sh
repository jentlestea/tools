#!/bin/sh

SOURCE_BRANCH=$INSTALL_SOURCE_BRANCH
REPOPATH=$INSTALL_REPO_PATH
time=$(date "+%Y-%m-%d")
log=$WORKON_HOME/log/$time.log

commitID=$1
currentDir=$PWD

TOOLSCRIPTDIR=$WORKON_HOME/tools/importfs

dir=$IFSPATH
if [ -z "$dir" ];then
	echo -1
	exit
fi

cat /dev/null > ./import.csv.tmp

for file in $(ls $dir)
do
	commitID=`bash -x $TOOLSCRIPTDIR/handleifs.sh $dir'/'$file $log`
	if [ "$commitID" != '0' ];then
		cd $REPOPATH #&> /dev/null
		commitMsg=`git show --format=%B $commitID $SOURCE_BRANCH  | head -n 1`
		type=`echo $commitMsg | sed -n -e 's/.*\[\(.*\)\].*/\1/p'`
		cd - &> /dev/null
		echo "$commitID $type" >> $currentDir/import.csv.tmp
	fi
done
echo 0
