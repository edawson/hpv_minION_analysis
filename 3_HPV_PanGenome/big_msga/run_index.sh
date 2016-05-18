
ind_str=""
vg=../../vg/bin/vg

for i in `ls | grep "msga.*vg" | sort -r`
do
    ind_str="$ind_str  $i"
done

$vg index -t 4 -x whole.xg -g whole.gcsa -k 16 $ind_str
