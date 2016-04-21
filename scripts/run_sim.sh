## Simulates reads from three different HPV
## lineage reference genomes. This simulation is
## run for a range of error rates.

## this data is then used as input to vg
## vectorize and clustering algorithms to
## demonstrate VG's ability to classify reads
## by genomic feature coverage.

vg=../vg-v1.1.0-1083-g618ce75

hpv_one=../hpv_1.fa
hpv_sixteen=../hpv_16.fa
hpv_two=../hpv_2.fa

node_len=50

num_reads=10000
read_len=7500
e_rate=$1
i_rate=$2
r_seed=110

function construct () {
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

for i in ${hpv_one} ${hpv_two} ${hpv_sixteen}
do
    my_vg=`construct ${i}`
    index ${my_vg}
    echo "Making reads with error rate $e_rate and indel rate $i_rate"
    my_reads=`sim_reads ${my_vg} ${num_reads} ${read_len} ${e_rate} ${i_rate}`
done


