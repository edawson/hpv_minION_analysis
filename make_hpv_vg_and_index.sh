input_ref=$1
input_vcf=$2
reads=$3

vg construct -t 4 -m 50 -r $input_ref -v $input_vcf > hpv.vg
vg index -x hpv.xg -g hpv.gcsa -k 16 hpv.vg
vg map -t 4 -B 200 -k 8 -f $reads -g hpv.gcsa -x hpv.xg > hpv.gam

