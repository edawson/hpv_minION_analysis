indir=$1
ind_str=""
vg=../../vg/bin/vg

for i in `ls $indir | grep "msga.*vg" | sort -r`
do
    ind_str="$ind_str  $indir/$i"
done

$vg index -t 4 -x whole.xg -g whole.gcsa -k 16 $ind_str
