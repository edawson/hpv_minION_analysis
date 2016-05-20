Testing a Pan-HPV Type/Lineage/Sublineage Identifier based on Mash
--------------
Eric T Dawson

## Mash
[Mash](https://github.com/marbl/Mash.git) is program for fast genome comparison based on MinHash.
MinHash works by comparing the kmer spaces of sets. The algorithm was originally used to detect
duplicate or near-duplicate web pages. Mash adapts it for use on genomic data, and it's proven to be
very useful (and impressive) in metagenomics.

## Creating a pan-genome HPV sketch 

## And an HPV subtype sketch...

## Identifying HPV types with Mash (with simulated data)

## Identifying HPV sublineage with Mash (with simulated data)

## Identifying type and subtype with Mash (using minION data)

## Pruning with a minimum kmer occurence filter

## Discussion

Mash performs admirably, even in the face of error. One of its shortcomings is that it is not
designed to deal with mixtures. One way to fix this would be to add kmer occurrence filtering
to runs with individual sequences.

Parameter tuning with Mash is very important. Mash is fast enough to make entire parameter sweeps
of the sample space possible in short amounts of time. However, this process is tedious to the user.

Mash easily determines HPV type, but because subtypes are more similar the MinHash algorithm is not
optimally suited to dealing with them.
