input=$1

vg=../../vg/bin/vg
vw=../../vw-8.20151121
graph=../hpv_16_panGraph.vg
index=../hpv_16_panGraph.xg
gcsa=../hpv_16_panGraph.gcsa

rm .cache
${vg} map -f ${input} -B 256 -GX .2 -t 2 -Z 1 -x ${index} -g ${gcsa} | \
    ${vg} vectorize -w -x ${index} - | \
    ${vw} --oaa 3 --ngrams 5 --passes=20 --threads  -f `basename ${input} .fq`.trained
