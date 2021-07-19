#!/bin/sh

if [[ `uname` == 'Darwin' ]];then
	sed -i '' '/CWORKON_HOME=/d' ~/.bashrc
	sed -i '' '/alias Question=/d' ~/.bashrc
	sed -i '' '/CPYTHONPATH=/d' ~/.bashrc
else
	sed -i '/CWORKON_HOME=/d' ~/.bashrc
	sed -i '/alias Question=/d' ~/.bashrc
	sed -i '/CPYTHONPATH=/d' ~/.bashrc
fi
source ~/.bashrc
