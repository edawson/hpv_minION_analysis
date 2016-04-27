input=$1

vg=../vg-v1.1.0-1083-g618ce75
vw=../vw-8.20151121
graph=hpv_16.vg
index=hpv_16.xg
gcsa=hpv_16.gcsa

rm .cache
${vg} map -f ${input} -B 256 -GX .2 -t 2 -Z 1 -x ${index} -g ${gcsa} | \
    ${vg} vectorize -w -x ${index} - | \
    ${vw} --oaa 3 --ngrams 5 --passes=20 --threads  -f `basename ${input} .fq`.trained
