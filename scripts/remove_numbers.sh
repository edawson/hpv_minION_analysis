while read line
do 
    echo `echo $line | sed "s/.vg_[0-9]*//g"`
done
