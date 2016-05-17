## Simulates reads from three different HPV
## lineage reference genomes. This simulation is
## run for a range of error rates.

## this data is then used as input to vg
## vectorize and clustering algorithms to
## demonstrate VG's ability to classify reads
## by genomic feature coverage.

vg=/home/eric/sandbox/hpv_minION_analysis/vg/bin/vg
scripts_dir=/home/eric/sandbox/hpv_minION_analysis/scripts

node_len=50

num_reads=1000
read_len=7500
e_rate=0.05
i_rate=0.10
r_seed=110

function construct() {
    ${vg} construct -m ${node_len} -r $1 > `basename $1 .fa`.vg;
    echo "`basename $1 .fa`.vg";
}

function sim_reads(){
    output="`basename $1 .vg`.$2reads.error$4.length$3.indel$5.txt";
    ${vg} sim -x `basename $1 .vg`.xg -f -n $2 -l $3 -e $4 -s ${r_seed} -i $5 $1 > $output;
    echo ${output};
}

function map () {
    ${vg} map -t 4 -x `basename $1 .vg`.xg -g `basename $1 .vg`.gcsa -r $2 > `basename $2 .txt`.gam;
    echo "`basename $2 .txt`.gam";
}

function index (){
    ${vg} index -x `basename $1 .vg`.xg -g `basename $1 .vg`.gcsa -k 16 $1;
}

i=$1

echo "Processing $i"
my_vg=`construct ${i}`
index ${my_vg}
echo "Making reads with error rate $e_rate and indel rate $i_rate"
seq 10 | parallel --will-cite -j 4 "${vg} sim -n ${num_reads} -l ${read_len} -s {} -x `basename ${my_vg} .vg`.xg ${my_vg} > {}.n${num_reads}.e${e_rate}.i${i_rate}.l${read_len}.reads.`basename $my_vg .vg`.txt"
echo "reads made. Making FASTQ."
python $scripts_dir/format_reads.py -i <(cat *n${num_reads}.e${e_rate}.i${i_rate}.l${read_len}.reads.`basename $my_vg .vg`.txt) -q ")" -n ${my_vg} > n${num_reads}.e${e_rate}.i${i_rate}.l${read_len}.reads.`basename $my_vg .vg`.fq
echo "FASTQs made for: $i"

