vg=~/sandbox/vg/bin/vg

hpv_sixteen=../hpv_16.fa

node_len=50

num_reads=1000
read_len=7500

bandwidth=20000

function construct () {
    ${vg} construct -m ${node_len} -r $1 > `basename $1 .fa`.vg;
    echo "`basename $1 .fa`.vg";
}

${vg} construct -r ${hpv_sixteen} -m ${node_len} > hpv_16.vg
${vg} index -x hpv_16.xg -k 16 -g hpv_16.gcsa hpv_16.vg


##hpv_16.1000reads.error0.0.length7500.indel0.0.txt

for error_rate in 0.0 0.01 0.05 0.15 0.25
do
    echo "Error: ${error_rate}"
    cat hpv_*error${error_rate}.*indel0.0.txt > tmpError.txt
    ${vg} map -t 4 -GX -B ${bandwidth} -r tmpError.txt -x hpv_16.xg -g hpv_16.gcsa | ${vg} vectorize -f -x hpv_16.xg - > hpv_16_Aligned.error${error_rate}.bandwidth${bandwidth}vecs.txt
done


for indel_rate in 0.0000 0.01 0.05 0.15 0.25
do
    echo "Indels: ${indel_rate}"
    #cat hpv_*error${error_rate}.*indel0.0.txt > tmpError.txt
     ${vg} map -t 4 -GX -B ${bandwidth} -r hpv_*error0.0.*indel${indel_rate}.txt -x hpv_16.xg -g hpv_16.gcsa | ${vg} vectorize -f -x hpv_16.xg - > hpv_16_Aligned.indel${indel_rate}.vecs.txt
done
