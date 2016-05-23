Testing a Pan-HPV Type/Lineage/Sublineage Identifier based on Mash
--------------
Eric T Dawson

## Mash
[Mash](https://github.com/marbl/Mash.git) is program for fast genome comparison based on MinHash.
MinHash works by comparing the kmer spaces of sets. The algorithm was originally used to detect
duplicate or near-duplicate web pages. Mash adapts it for use on genomic data, and it's proven to be
very useful (and impressive) in metagenomics.

## Creating a pan-genome HPV sketch 
To demonstrate, how simple it is to create pangenome-like structures, let's make a sketch of our HPV genomes
using mash:  
`mash sketch -s 1000 -k 21 -o HPV_pan.sketch.msh ref/*.fa*`

This is in the makefile as : `make HPV_pan.sketch.msh`


## And an HPV subtype sketch...
`make HPV_16.sketch.msh`

## Identifying HPV types with Mash (with simulated data)
We'll now use the `mash dist` command to find genomes in our sketch that are most similar to our simulated HPV16
reads:  
`make HPV16_type_msh_pred.txt`

## Identifying HPV sublineage with Mash (with simulated data)
Now we'll try to identify which subtype our HPV16 reads came from. We generated a sketch of the HPV16 variants earlier,
so all we have to do is run `mash dist` again:  
`make HPV16_subtype_msh_pred.txt`

## Identifying type and subtype with Mash (using minION data)
Our minION data is from two isolates of HPV16 (1205 and 1507). They differ by 95 SNPs, 1 dinucleotide polymoprhism, 1 tetranucleotide polymorphism, and 1 single basepair insertion. They are 99.98% identical in
their sequences (the HPV16 reference is 7905bp long). Our nanopore amplicons are 7734bp long (because of primer sequences). They
vary in their percent identity to the reference; BLAST returns 88% max identity (57.6% coverage) for one read I tried and no matches
for three others. Your mileage may vary.

I'll just go ahead and spoil the fun now:
        ../bin/mash dist -r HPV_pan.sketch.msh hpv_minION_reads.fastq | sort -k3 -n | head -n 20
        Estimated genome size: 1.65117e+07
        Estimated coverage:    1.158
        ref/GammapapillomavirusR3a_.gb293596086.fa  hpv_minION_reads.fastq  1   1   0/1000
        ref/Genitaltype_.gb60955.fa hpv_minION_reads.fastq  1   1   0/1000
        ref/Human100_.gb238623442.fa    hpv_minION_reads.fastq  1   1   0/1000
        ref/Human101_.gb71726703.fa hpv_minION_reads.fastq  1   1   0/1000

Without kmer filtering, the Mash defaults (sketch size 1000, k=21) are insufficient for classifying the minION reads.
The `-r` option tells Mash that the input data is a read set; the problem with this is that Mash does not yet support
mixtures of data, so our mixed set will return only a single prediction.


Let's do a parameter sweep to determine an optimal kmer/sketch size. The following runs a nested loop to check
kmer sizes of 8, 10, 15 and 18 and sketch sizes of 1000, 3000, 7000 and 10000:  
`make minIONs_type_s10000_k18_pred.txt`

What we see is that we don't see HPV16 in the top 20 predictions until we get to k=15 and s=3000. Even at k=18
and s=10000, we only see 3 matching kmer hashes in our set. However, our p-value is significant and we are now predicting
the correct class.


## Pruning with a minimum kmer occurence filter
Let's use Mash's kmer counting features to remove low-frequency kmers from the readset sketch. This will hopefully remove kmers
that might be occurring by chance.

`make minIONs_subtype_s10000_k18_m40_pred.txt`

This will run another loop, but will increase the minimum kmer occurrence from 1 to 2, 10, 20, 40 and 100.

        Minimum kmer occurence: 1

        Estimated genome size: 1.505e+07
        Estimated coverage:    1.2647
        ref/Human16_PPH16.gb333031.fa   hpv_minION_reads.fastq  0.41216 2.52907e-10     3/10000
        ref/Human18_.gb60975.fa hpv_minION_reads.fastq  0.473183        0.00114209      1/10000
        ref/Human201_.gb870702425.fa    hpv_minION_reads.fastq  0.473183        0.0010599       1/10000
        ref/Human915_.gb371486228.fa    hpv_minION_reads.fastq  0.473183        0.00104945      1/10000
        ref/GammapapillomavirusR3a_.gb293596086.fa      hpv_minION_reads.fastq  1       1       0/10000

        Minimum kmer occurence: 2

        Estimated genome size: 1.18305e+06
        Estimated coverage:    5.2489
        ref/Human16_PPH16.gb333031.fa   hpv_minION_reads.fastq  0.242483        3.25362e-278    64/10000
        ref/Human31_PPH31A.gb333048.fa  hpv_minION_reads.fastq  0.41216 2.49047e-10     3/10000
        ref/Human52_.gb397038.fa        hpv_minION_reads.fastq  0.41216 2.51871e-10     3/10000
        ref/Human58_PPH58.gb222386.fa   hpv_minION_reads.fastq  0.41216 2.40884e-10     3/10000
        ref/Human26_.gb396956.fa        hpv_minION_reads.fastq  0.43468 6.44143e-07     2/10000

        Minimum kmer occurence: 10

        Estimated genome size: 81599.4
        Estimated coverage:    39.6848
        ref/Human16_PPH16.gb333031.fa   hpv_minION_reads.fastq  0.102794        0       853/10000
        ref/Human35H_.gb396997.fa       hpv_minION_reads.fastq  0.299111        1.05039e-91     23/10000
        ref/Human31_PPH31A.gb333048.fa  hpv_minION_reads.fastq  0.301575        2.51817e-87     22/10000
        ref/Human52_.gb397038.fa        hpv_minION_reads.fastq  0.330752        3.12302e-49     13/10000
        ref/Human58_PPH58.gb222386.fa   hpv_minION_reads.fastq  0.351159        3.86837e-33     9/10000

        Minimum kmer occurence: 20

        Estimated genome size: 33882.6
        Estimated coverage:    75.9063
        ref/Human16_PPH16.gb333031.fa   hpv_minION_reads.fastq  0.0632226       0       1908/10000
        ref/Human35H_.gb396997.fa       hpv_minION_reads.fastq  0.263189        1.41839e-188    44/10000
        ref/Human31_PPH31A.gb333048.fa  hpv_minION_reads.fastq  0.284388        4.55914e-124    30/10000
        ref/Human58_PPH58.gb222386.fa   hpv_minION_reads.fastq  0.340022        1.05536e-41     11/10000
        ref/Human56_.gb397053.fa        hpv_minION_reads.fastq  0.345312        1.28267e-37     10/10000

        Minimum kmer occurence: 40

        Estimated genome size: 17121.4
        Estimated coverage:    125.113
        ref/Human16_PPH16.gb333031.fa   hpv_minION_reads.fastq  0.0386627       0       3321/10000
        ref/Human35H_.gb396997.fa       hpv_minION_reads.fastq  0.245133        6.4317e-274     61/10000
        ref/Human31_PPH31A.gb333048.fa  hpv_minION_reads.fastq  0.267095        1.53005e-177    41/10000
        ref/Human52_.gb397038.fa        hpv_minION_reads.fastq  0.315871        4.98404e-68     17/10000
        ref/Human33_PPH33CG.gb333049.fa hpv_minION_reads.fastq  0.319234        1.02708e-63     16/10000

        Minimum kmer occurence: 100

        Estimated genome size: 7981.92
        Estimated coverage:    197.766
        ref/Human16_PPH16.gb333031.fa   hpv_minION_reads.fastq  0.0312988       0       3979/10000
        ref/Human35H_.gb396997.fa       hpv_minION_reads.fastq  0.228813        0       82/10000
        ref/Human31_PPH31A.gb333048.fa  hpv_minION_reads.fastq  0.257237        3.20132e-222    49/10000
        ref/Human33_PPH33CG.gb333049.fa hpv_minION_reads.fastq  0.309703        2.42529e-79     19/10000
        ref/Human69_.gb6970418.fa       hpv_minION_reads.fastq  0.315871        1.97876e-70     17/10000

By m=2, we can see that the effects of low abundance kmers are being minimized. We see similar effects for subtypes:

        Minimum kmer occurence: 1

        Estimated genome size: 1.63527e+07
        Estimated coverage:    1.19786
        hpv16/Human16_.gb27463084.fa    hpv_minION_reads.fastq  0.388603    1.2574e-05  1/7000
        hpv16/GammapapillomavirusR3a_.gb293596086.fa    hpv_minION_reads.fastq  1   1   0/7000
        hpv16/Genitaltype_.gb60955.fa   hpv_minION_reads.fastq  1   1   0/7000
        hpv16/Human100_.gb238623442.fa  hpv_minION_reads.fastq  1   1   0/7000
        hpv16/Human101_.gb71726703.fa   hpv_minION_reads.fastq  1   1   0/7000

        Minimum kmer occurence: 2

        Estimated genome size: 896686
        Estimated coverage:    5.39157
        hpv16/Human16_.gb27463084.fa    hpv_minION_reads.fastq  0.191731    0   63/7000
        hpv16/Human16_PPH16.gb333031.fa hpv_minION_reads.fastq  0.195635    0   58/7000
        hpv16/Human16_.gb33330936.fa    hpv_minION_reads.fastq  0.196456    0   57/7000
        hpv16/Human16_.gb399525822.fa   hpv_minION_reads.fastq  0.196456    0   57/7000
        hpv16/Human16_.gb399526191.fa   hpv_minION_reads.fastq  0.198143    0   55/7000

        Minimum kmer occurence: 10

        Estimated genome size: 62267.4
        Estimated coverage:    38.1373
        hpv16/Human16_.gb27463084.fa    hpv_minION_reads.fastq  0.0764079   0   782/7000
        hpv16/Human16_PPH16.gb333031.fa hpv_minION_reads.fastq  0.0782013   0   750/7000
        hpv16/Human16_.gb399525633.fa   hpv_minION_reads.fastq  0.0786628   0   742/7000
        hpv16/Human16_.gb399525822.fa   hpv_minION_reads.fastq  0.079543    0   727/7000
        hpv16/Human16_.gb33330936.fa    hpv_minION_reads.fastq  0.0797214   0   724/7000

        Minimum kmer occurence: 20

        Estimated genome size: 27248.9
        Estimated coverage:    69.4156
        hpv16/Human16_.gb27463084.fa    hpv_minION_reads.fastq  0.044583    0   1707/7000
        hpv16/Human16_.gb399525633.fa   hpv_minION_reads.fastq  0.0478612   0   1568/7000
        hpv16/Human16_PPH16.gb333031.fa hpv_minION_reads.fastq  0.0480105   0   1562/7000
        hpv16/Human16_.gb399525822.fa   hpv_minION_reads.fastq  0.0485127   0   1542/7000
        hpv16/Human16_.gb33330936.fa    hpv_minION_reads.fastq  0.0493326   0   1510/7000

        Minimum kmer occurence: 40

        Estimated genome size: 14429.4
        Estimated coverage:    106.946
        hpv16/Human16_.gb27463084.fa    hpv_minION_reads.fastq  0.0265998   0   2804/7000
        hpv16/Human16_.gb399525822.fa   hpv_minION_reads.fastq  0.031103    0   2462/7000
        hpv16/Human16_.gb56462978.fa    hpv_minION_reads.fastq  0.0328138   0   2346/7000
        hpv16/Human16_.gb29468132.fa    hpv_minION_reads.fastq  0.0329051   0   2340/7000
        hpv16/Human16_.gb399525633.fa   hpv_minION_reads.fastq  0.0329509   0   2337/7000

        Minimum kmer occurence: 100

        Estimated genome size: 5914.07
        Estimated coverage:    172.69
        hpv16/Human16_.gb27463084.fa    hpv_minION_reads.fastq  0.0224307   0   3177/7000
        hpv16/Human16_.gb399525822.fa   hpv_minION_reads.fastq  0.027651    0   2719/7000
        hpv16/Human16_.gb399526191.fa   hpv_minION_reads.fastq  0.0280962   0   2684/7000
        hpv16/Human16_.gb33330945.fa    hpv_minION_reads.fastq  0.0286795   0   2639/7000
        hpv16/Human16_.gb56462978.fa    hpv_minION_reads.fastq  0.0288504   0   2626/7000


However, this method still needs to be extended to handle mixtures to accurately handle our
samle set.

## Discussion

Mash performs admirably at classifying our read set. We'd like to see it extended to work on mixtures
so that it's better able to handle our future data, but overall it is rather impressive.

Parameter tuning with Mash is very important. Mash is fast enough to make entire parameter sweeps
of the sample space possible in short amounts of time. However, this process is tedious to the user.

The MinHash algorithm is not designed to distinguish between things that are only subtly different, so
if we want to get more fine-grained in distinguishing subtypes or if we start trying to find novel types
we may run into issues.

We would also like to implement an algorithm that works with ONT's read-until functionality. This would
likely involve a minimum amount of software engineering.
