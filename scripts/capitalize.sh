
for i in ../hpv_1.fa ../hpv_2.fa ../hpv_16.fa
do
     cat $i | tr [:lower:] [:upper:] > tmp && mv tmp $i
done
