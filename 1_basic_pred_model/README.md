Classifying HPV strains with vowpal-wabbit
-------------
Eric T Dawson

## Problem setup
Given a single HPV graph and a set of different reference genomes, can we
use machine learning to predict which genome a simulated read came from?


[vg](https:/github.com/vgteam/vg.git) now includes a `vectorize` command to transform mappings
to simple vectors. We'll use one of these vector formats as input to vowpal-wabbit,
a powerful machine learning package from John Langford.

## First: simulate some reads, map them to a reference, and vectorize them.
To generate the vectors for input to vw, try:  
`make train_me.vecs.wabbit`



What happens: we first generate a single graph from the HPV16 reference genome, circularize it (as the HPV genome is circular) and index it.

        $(VG) construct -r $(fasta_file) -v $(vcf_file) -m 50 > $(base_name).vg
        $(VG) circularize -p HPV16Ref $(base_name).vg > $(base_name).circ.vg
        $(VG) index -x $(base_name).circ.xg -g $(base_name).circ.gcsa -k 16 $(base_name).circ.vg

We then simulate 1000 reads from each of the HPV1, HPV2, and HPV16 reference genomes. These
reads are 7000bp long, have an error rate of 5% and an indel rate of 10%. I've encapsulated a lot
of this away, but the make_reads script can show you the simulation process in detail if you're interested.

	../scripts/make_reads.sh hpv_1.fa
	../scripts/make_reads.sh hpv_2.fa
	../scripts/make_reads.sh hpv_16.fa


Next we'll concatenate all our training data together, format the identifier lines with the `remove_numbers.sh` script,
and shuffle the fastq records:

	cat n100.e0.05.i0.10.l7500.reads.hpv_* | ../scripts/remove_numbers.sh | ../scripts/shuf.py > all.fq

Now we have a dataset containing 3000 fastq records. Let's map them to our HPV16 reference
and vectorize them.

    vg map -GX .5 -A 4 -B 128 -f all.fq -x $(base_name).circ.xg -g $(base_name).circ.gcsa > aln.gam
    vg vectorize -w -a -x $(base_name).circ.xg aln.gam > aln.vecs.txt

## Training and testing a learning model on our vectors 
To train and test a model:  

        make test_pred.txt

Now that we have vectors, we can take a subset and train our model on it. We'll use 10% (300 / 3000 vectors) for our training set:  
        
        cat aln.vecs.txt | shuf | head -n 1000 | vw --oaa 3 --binary --ngram 5 --passes=20 --threads  -f trained.model --cache_file .cache

And now we can test on our whole dataset and make a confusion matrix to see what they're classified as:  

        cat aln.vecs.txt | vw -i trained.model -p /dev/stdout | tee pred.txt | python ../scripts/make_confusion_matrix.py -c mappings.text 

And we do pretty well:

                    hpv_1   hpv_16  hpv_2
            hpv_1   1000    0       0
            hpv_16  0       1000    0
            hpv_2   0       0       1000
