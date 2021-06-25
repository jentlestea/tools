#!/bin/bash

export WORKON_HOME=`pwd`
export PYTHONPATH=$PYTHONPATH:$WORKON_HOME:$WORKON_HOME/proto
alias Question='python3 '$WORKON_HOME'/grab.py'
