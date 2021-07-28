#!/bin/bash

time=$(date "+%Y-%m-%d")
DATABASEDIR=$WORKON_HOME/dataBase
SCRIPTDIR=$WORKON_HOME/script
log=$WORKON_HOME/log/$time.log
cd $SCRIPTDIR
echo 'Start refresh candidates... time:['$time']' >> $log

REPOPATH=$INSTALL_REPO_PATH
TARGET_BRANCH=$INSTALL_TARGET_BRANCH
SOURCE_BRANCH=$INSTALL_SOURCE_BRANCH

if [ ! -d $REPOPATH ];then
	echo 'ERROR: '$REPOPATH" does not exist, skipping..." >> $log
	echo 0
	exit
fi

cd $INSTALL_REPO_PATH
#branches=`git branch`
#hastbranch=`echo branches | grep $INSTALL_TARGET_BRANCH`
if [ `git rev-parse --verify $INSTALL_TARGET_BRANCH` ];then
	echo 'SUCCESS: branch '$INSTALL_TARGET_BRANCH' check pass.' >> $log
else
	echo 'ERROR: branch '$INSTALL_TARGET_BRANCH' not exit.' >> $log
	echo 0
	exit
fi

if [ `git rev-parse --verify $INSTALL_SOURCE_BRANCH` ];then
	echo 'SUCCESS: branch '$INSTALL_SOURCE_BRANCH' check pass.' >> $log
else
	echo 'ERROR: branch '$INSTALL_SOURCE_BRANCH' not exit.' >> $log
	echo 0
	exit
fi
cd - 2>&1 >/dev/null

[ -r tag.conf ] && . ./tag.conf || echo " tag.conf file not exist" >> $log

TTAGBASE=$TARGETBASE
TAGFROM=$SOURCEFROM
TAGTO=$SOURCETO
function version_le() { test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" == "$1"; }
if version_le $TAGTO $TAGFROM;then
    echo 'WARN: Totag:'$TAGTO' Fromtag:'$TAGFROM' check failed' >> $log
fi

cd $REPOPATH
#for commit in $(git rev-list $SOURCE_BRANCH $TAGFROM..$TAGTO)
git pull question $SOURCE_BRANCH &> /dev/null
#Note! TODO we only pull question from import.csv but not here
#git log --oneline $SOURCE_BRANCH $TAGFROM..$TAGTO | awk ' ''{print $1}' > .tmp
#Plugin extra commitIDs
cat /dev/null > $REPOPATH/.tmp
if [ -f "$IMPORT_COMMIT_FILE" ];then
	cat $IMPORT_COMMIT_FILE >> $DATABASEDIR/summary/total.csv
	cat $IMPORT_COMMIT_FILE | awk ' ''{print $1}' > .itmp

	cat $IMPORT_COMMIT_FILE | while read line
	do
		commitID=`echo $line | awk ' ''{print $1}'`
		found=`git log --oneline $SOURCE_BRANCH | grep "$commitID"`
		if [ -z "$found" ];then
			sed -i '/'"$commitID"'/d' .itmp
			echo $commitID" does not in branch "$SOURCE_BRANCH >> $log
		fi
	done
	cat .itmp >> .tmp
	rm .itmp
fi
cd - 2>&1 >/dev/null
#sort total.csv .tmp
sort -u $DATABASEDIR/summary/total.csv > .total.csv
cat .total.csv > $DATABASEDIR/summary/total.csv
rm .total.csv
sort -u $DATABASEDIR/.tmp > ..tmp
cat ..tmp > $DATABASEDIR/.tmp
rm ..tmp

cat $REPOPATH/.tmp > .prepareToMergePatches.tmp
rm $REPOPATH/.tmp

cd $REPOPATH
targetHeadCommits=`git rev-list -1 $TARGET_BRANCH`
cd - 2>&1 >/dev/null

cd $REPOPATH
#TODO
git pull openEulerKernel $TARGET_BRANCH &> /dev/null
cd - 2>&1 >/dev/null

scanPatchesHasMerged(){
	cd $REPOPATH
	#git checkout $TARGET_BRANCH
	git log --oneline $targetHeadCommits..$TARGET_BRANCH | awk ' ''{print $1}' > .tmp
	sed -i "1d" .tmp
	cd - 2>&1 >/dev/null
	cat /$REPOPATH/.tmp > .mergedCommitIDs.tmp

	cd $REPOPATH
	cat /$REPOPATH/.tmp | while read line
	do
		commitMsg=`git show --format=%B $line $SOURCE_BRANCH | head -n 1`
		isLTS=`echo $commitMsg | grep '##LTS##'`
		if [ -n "$isLTS" ];then
			author=`git log $line -1 $TARGET_BRANCH | sed -n -e 's/.*Author: \(.*\)/\1/p'`
			echo $author >> $DATABASEDIR/person/LTSList
		fi
	done
	cd - 2>&1 >/dev/null

    # it has been merged
    cat .mergedCommitIDs.tmp >> $DATABASEDIR/history/$time.pchs

    # for UI display
	#Insert csv head
	if [ ! -f $DATABASEDIR/record/newMerged$time.record ];then
		echo "author commit bugzilla score" > $DATABASEDIR/record/newMerged$time.record
	fi
    cat .mergedCommitIDs.tmp | while read line
    do
		cd $REPOPATH
		author=`git log $line -1 $TARGET_BRANCH | sed -n -e 's/.*Author: \(.*\)/\1/p'`
		bugzilla=`git log $line -1 $TARGET_BRANCH | sed -n -e 's/.*bugzilla: \(.*\)/\1/p'`
		cd - 2>&1 >/dev/null
		#get score
		score=`cat $DATABASEDIR/summary/total.csv | grep $bugzilla | awk ' ''{print $4}'`
		echo $author' '$line' '$bugzilla' '$score >> $DATABASEDIR/record/newMerged$time.record
    done
	sort -u $DATABASEDIR/record/newMerged$time.record > .recordTmp
	cat .recordTmp > $DATABASEDIR/record/newMerged$time.record
	rm .recordTmp

	cat $DATABASEDIR/record/newMerged$time.record >> $OUTPUT_REPORT_DIR/$time.report 2>&1 > /dev/null

    # drop this commits from active.pchs to history, it has been merged
    cat .mergedCommitIDs.tmp | while read line
    do
		# patch body
		# commit 45cb6653b0c355fc1445a8069ba78a4ce8720511
		targetCommitID=$line

		cd $REPOPATH
		bugzilla=`git log $targetCommitID -1 $TARGET_BRANCH | sed -n -e 's/.*bugzilla: \(.*\)/\1/p' | head -n 2 | tail -n +2`
		sourceCommitID=`cat $DATABASEDIR/summary/total.csv | grep $bugzilla | awk ' ''{print $1}'`
		cd - 2>&1 >/dev/null

		sed -i '/'"$sourceCommitID"'/d' $DATABASEDIR/active.pchs
    done
    rm -f .mergedCommitIDs.tmp

	# drop this source commits if it has been merged
    cat .prepareToMergePatches.tmp | while read line
    do
		commitID=$line
		cd $REPOPATH
		#commitMsg=`git show --format=%B $commitID $SOURCE_BRANCH  | head -n 1`
		#found=`git log --oneline $TTAGBASE..HEAD | grep "$commitMsg"`
		bugzilla=`cat $DATABASEDIR/summary/total.csv | grep $commitID | awk ' ''{print $3}'`
		found=`git log $TTAGBASE..$TARGET_BRANCH $TARGET_BRANCH | grep $bugzilla`
		cd - 2>&1 >/dev/null
		if [ -n "$found" ];then
			sed -i '/'"$commitID"'/d' .prepareToMergePatches.tmp
		fi
    done
}
scanPatchesHasMerged
putPatchesToDatabase(){
    cat .prepareToMergePatches.tmp > $DATABASEDIR/active.pchs.new
    rm -f .prepareToMergePatches.tmp
}
putPatchesToDatabase

c=`cat $DATABASEDIR/active.pchs.new | wc -l`
echo 'SUCCESS: Flush patches count: '$c >> $log

# it has been in active list
dropActivePchs(){
	cat $DATABASEDIR/active.pchs | while read line
	do
		sed -i '/'"$line"'/d' $DATABASEDIR/active.pchs.new
	done
}
dropActivePchs

createBugzilla(){
    echo 'Prepare to create bugzilla...' >> $log
    cat $DATABASEDIR/active.pchs.new | while read line
    do
		#bugID=0 #`perl ./ipatches2ol.pl -f $DATABASEDIR/active.pchs.new`
		#if [ $bugID -ne -1 ];then
		#	echo 'SUCCESS: create bugzilla, '$line' '$bugID >> $log
		#	echo $line' '$bugID >> $DATABASEDIR/candidates
		bugzilla=`cat $DATABASEDIR/summary/total.csv | grep $line | awk ' ''{print $3}'`
		if [ -n "$bugzilla" ];then
			echo "SUCCESS: scan bugzilla, "$line" "$bugzilla >> $log
			echo $line' '$bugzilla >> $DATABASEDIR/candidates
		else
			sed -i '/'"$line"'/d' $DATABASEDIR/active.pchs.new
		fi
    done

    echo 'Create bugzilla end' >> $log
}
createBugzilla

mergeActivePatches(){
    cat $DATABASEDIR/active.pchs.new >> $DATABASEDIR/active.pchs
    rm -f $DATABASEDIR/active.pchs.new
}
mergeActivePatches

# if not in active.pchs, drop it from candidates
cleanCandidates(){
    cat $DATABASEDIR/candidates | while read line
	do
		commitID=`echo $line | awk ' ''{print $1}'`
		found=`cat $DATABASEDIR/active.pchs | grep "$commitID"`
		if [ -z $found ];then
			sed -i 's#'"$line"'##' $DATABASEDIR/candidates
		fi
	done
	sed -i '/^$/d' $DATABASEDIR/candidates
}
cleanCandidates

# if not in candidates, drop it from frozen.usr
cleanFrozen(){
	cat $DATABASEDIR/frozen.usr | while read line
	do
		commitID=`echo $line | awk ' ''{print $1}'`
		found=`cat $DATABASEDIR/candidates | grep "$commitID"`
		if [ -z "$found" ];then
			sed -i 's#'"$line"'##' $DATABASEDIR/frozen.usr
		fi
	done
	sed -i '/^$/d' $DATABASEDIR/frozen.usr
}
cleanFrozen

echo 'SUCCESS: refresh candidates OK' >> $log
rm -f .candidates.tmp

cat /dev/null > $DATABASEDIR/mergeConflicts
judgeMergeConflicts(){
	cd $REPOPATH
 	cat $DATABASEDIR/active.pchs | while read line
	do
		conflict=`git show --format=%B $line $SOURCE_BRANCH | head -n 1 | grep '##Conflict##'`
		if [ -n "$conflict" ];then
			echo $line >> $DATABASEDIR/mergeConflicts
		fi
	done
	cd - 2>&1 >/dev/null
}
judgeMergeConflicts

rm REPOPATH/.tmp &> /dev/null
rm .prepareToMergePatches.tmp &> /dev/null
rm .tmp &> /dev/null
rm .itmp &> /dev/null
echo 0
