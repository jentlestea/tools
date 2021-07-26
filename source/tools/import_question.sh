#!/bin/sh

if [ -f $IMPORT_COMMIT_FILE ];then
	mv $IMPORT_COMMIT_FILE $IMPORT_COMMIT_FILE.old
fi

