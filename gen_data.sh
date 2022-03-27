#!/bin/bash

url='http://0.0.0.0:8080/'

if [ $# -lt 2 ]; then
    echo $0 op size
    exit
fi

op=$1
size=$2

if [ ${op} == 'write' ]; then
    file=`cat ${size}`
    cmd=${url}${op}/${size}/${file}
fi

echo ${cmd} > ${op}_${size}
