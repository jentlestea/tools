#!/bin/bash

echo $#
if [ $# != 1 ];then
	exit
fi

QCDIR=$1

if [ -f '/etc/bash_completion.d/qcc.sh' ];then
	exit
fi
cp $QCDIR/qcc.sh /etc/bash_completion.d
source /etc/bash_completion.d/qcc.sh

if [ -f '/etc/profile.d/qc.sh' ];then
	exit
fi

touch /etc/profile.d/qc.sh
echo "QCDIR=$QCDIR" >> /etc/profile.d/qc.sh
echo "export QCWORKON_HOME=$QCDIR" >> /etc/profile.d/qc.sh
echo "alias Question='python3 $QCDIR/grab.py'" >> /etc/profile.d/qc.sh

