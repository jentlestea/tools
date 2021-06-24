#!/bin/bash

time=$(date "+%Y-%m-%d")
DATABASEDIR=$WORKON_HOME/dataBase
SCRIPTDIR=$WORKON_HOME/script
log=$SCRIPTDIR/log/$time.log
cd $SCRIPTDIR
echo 'Start refresh candidates... time:['$time']' >> $log

REPOPATH=$WORKON_HOME/../repo
TARGET_BRANCH=workspace
SOURCE_BRANCH=repo.linux.5.10.y

[ -r tag.conf ] && . ./tag.conf || echo " tag.conf file not exist"

TTAGBASE=$TARGETBASE
TAGFROM=$SOURCEFROM
TAGTO=$SOURCETO
function version_le() { test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" == "$1"; }
if version_le $TAGTO $TAGFROM;then
    echo 'ERROR: '$TAGTO' is older than '$TAGFROM >> $log
    echo -1
fi

cd $REPOPATH
#for commit in $(git rev-list $SOURCE_BRANCH $TAGFROM..$TAGTO)
git log --oneline $SOURCE_BRANCH $TAGFROM..$TAGTO | awk ' ''{print $1}' > .tmp
cd - 2>&1 >/dev/null

cat $REPOPATH/.tmp > .prepareToMergePatches.tmp

cd $REPOPATH
targetHeadCommits=`git rev-list -1 $TARGET_BRANCH`
cd - 2>&1 >/dev/null

cd $REPOPATH
#TODO
#git pull openeuler $TARGET_BRANCH
cd - 2>&1 >/dev/null

scanPatchesHasMerged(){
	cd $REPOPATH
	git log --oneline $TARGET_BRANCH $targetHeadCommits..HEAD | awk ' ''{print $1}' > .tmp
	cd - 2>&1 >/dev/null
	cat /$REPOPATH/.tmp > .mergedCommitIDs.tmp

    # it has been merged
    cat .mergedCommitIDs.tmp >> $DATABASEDIR/history/$time.pchs

    # for UI display
    cat .mergedCommitIDs.tmp | while read line
    do
		cd $REPOPATH
		author=`git log $line -1 $TARGET_BRANCH | sed -n -e 's/.*Author: \(.*\)/\1/p'`
		bugzilla=`git log $line -1 $TARGET_BRANCH | sed -n -e 's/.*bugzilla: \(.*\)/\1/p'`
		cd - 2>&1 >/dev/null
		echo $author' '$line' '$bugzilla > $DATABASEDIR/newMerged.record
    done

    # drop this commits from active.pchs to history, it has been merged
    cat $DATABASEDIR/history/$time.pchs | while read line
    do
		# patch body
		# commit 45cb6653b0c355fc1445a8069ba78a4ce8720511
		targetCommitID=$line

		cd $REPOPATH
		sourceCommitID=`git log $targetCommitID -1 $TARGET_BRANCH | sed -n -e 's/.*commit \(.*\)/\1/p' | head -n 2 | tail -n +2`
		cd - 2>&1 >/dev/null

		sed -i '/'"$sourceCommitID"'/d' $DATABASEDIR/active.pchs
    done

	# drop this commits if it has been merged
    cat .prepareToMergePatches.tmp | while read line
    do
		commitID=$line
		cd $REPOPATH
		commitMsg=`git show --format=%B $commitID $SOURCE_BRANCH  | head -n 1`
		found=`git log --oneline $TTAGBASE..HEAD | grep "$commitMsg"`
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
		bugID=0 #`perl ./ipatches2ol.pl -f $DATABASEDIR/active.pchs.new`
		if [ $bugID -ne -1 ];then
			echo 'SUCCESS: create bugzilla, '$line' '$bugID >> $log
			echo $line' '$bugID >> $DATABASEDIR/candidates
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
		found=`cat $DATABASEDIR/candidates | grep "$line"`
		if [ -z $found ];then
			sed -i 's#'"$line"'##' $DATABASEDIR/frozen.usr
		fi
	done
	sed -i '/^$/d' $DATABASEDIR/frozen.usr
}
cleanFrozen

echo 'SUCCESS: refresh candidates OK' >> $log
rm -f .candidates.tmp

echo 0
