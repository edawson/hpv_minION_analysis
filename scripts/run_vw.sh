vw=../
vg=../

training_vecs=

test_vecs=

cat $training_vecs  | ${vw} --oaa --cache_file vw.cache --passes 20 --binary -c --ngram 5 -f hpv_model_3Genome.vw 

cat $test_vecs  | ${vw} -t -i hpv_model_3Genome.vw -p /dev/stdout
