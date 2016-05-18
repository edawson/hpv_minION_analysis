vg=
indir=$1
hpv_pan="hpv_pan"
## Precluster with mash
#./precluster_with_mash.sh $indir

## perform MSGA on preclustered samples
#./msga_preclustered.py -i 
## correct ID space
$vg ids -j $(ls $indir | grep ".vg$" | sort)
## cat graphs
cat $(ls $indir | grep ".vg$" | sort -r)

