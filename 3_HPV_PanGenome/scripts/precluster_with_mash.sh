mash=../Mash/mash
indir=$1
N=20
##Sketch only 7k because any more than that is too many for some of the shorter genomes.
sketch_size=7000
## Use k=16 because these genomes are short.
kmer_size=16

ofi="${indir}_close_${N}.txt"

all_ref="${indir}_k${kmer_size}_s${sketch_size}.msh"

usage(){
    echo "Usage: ./precluster_with_mash <DirectoryWithFASTAs>"
    echo "the only argument is a directory containing a bunch of fasta files"
}

if [[ ! -d $indir ]]; then
    usage
    exit
fi

if [[ -e $all_ref ]]; then
    rm $all_ref
fi

## Step one: sketch all references into a single sketch
$mash sketch -k $kmer_size -s $sketch_size -o `basename $all_ref .msh` $(for i in `ls $indir | grep ".fa$\|.fasta$"`; do echo -n " ${indir}/$i"; done)

## Step two: compute pairwise distances to all refs, then output the top N
if [[ -e $ofi ]]; then
    rm $ofi
fi

for i in $(ls $indir | grep ".fa$\|.fasta$")
do
    $mash dist $all_ref ${indir}/$i | sort -n -k3 | head -n $N >> $ofi
done

>&2 echo "Preclusterings generated and stored in  $ofi".
