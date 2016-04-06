## Simulates reads from three different HPV
## lineage reference genomes. This simulation is
## run for a range of error rates.

## this data is then used as input to vg
## vectorize and clustering algorithms to
## demonstrate VG's ability to classify reads
## by genomic feature coverage.

hpv_one=../hpv_1.fa
hpv_sixteen=../hpv_16.fa
hpv_two=../hpv_2.fa

num_reads=1000
read_len=7500
e_rate=0.0
r_seed=110

function construct () {
    ../vg/bin/vg construct -r $1 > `basename $1 .fa`.vg;
}

function sim_reads(){
    ../bin/vg sim -f -n $1 -l $2 -e $3 -r ${r_seed} -i $5 $4 > `basename $4 .vg`.reads.error$3.length$2.indel$5.txt;
}

function map () {
    ../bin/vg map -t 4 > $4;
}

for i in ${hpv_one} ${hpv_two} ${hpv_sixteen}
do
    construct ${i}
done
