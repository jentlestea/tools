#!/bin/bash

if [ -n "$1" ];then
	echo $1 > ip.conf
fi

echo "export CWORKON_HOME=`pwd`" >> ~/.bashrc
echo "export CPYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/proto" >> ~/.bashrc
echo "alias Question='python3 `pwd`/grab.py'" >> ~/.bashrc
