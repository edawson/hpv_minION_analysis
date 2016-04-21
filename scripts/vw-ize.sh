#!/usr/bin/env bash


control_c(){
    exit $?
}



## currently just greps the last digits after hpv. pretty crude.

name_to_cat (){
    ret=$(echo "$1" | cut -f 2 -d "_")
    echo $ret
}

gen_features (){
    ret=""
    count=0
    for i in $1
    do
        count=$(($count + 1))
        ret+="${count}:$(($i)) "
    done
    echo ${ret}
}


count=0
trap control_c INT SIGTERM SIGINT
while read line
do
    label="$(echo $line | cut -f 1 | grep -o "hpv_[0-9]\{1,10\}")"
    category=$(name_to_cat $label)
    features=`gen_features "$(echo $line | cut -f2- -d" ")"`
    echo "${category} 1.0 '$label |vector ${features}"
done
