#!/bin/sh

BKPATH=~/oqserver/backend
time=$(date "+%Y-%m-%d")

mkdir -p $BKPATH/$time

BK1=$WORKON_HOME/dataBase
BK2=$WORKON_HOME/log

if [[ ! -d $BK1 ]] || [[ ! -d $BK2 ]];then
	echo -1
fi

tar -zxvf $time.bk1.tar.gz $BK1/*
tar -zxvf $time.bk2.tar.gz $BK2/*

echo 0
