## Converts the simulated reads to fastqs

for i in hpv_1 hpv_16 hpv_2
do
    echo ${i}
    for j in `ls | grep "${i}\..*reads.*\.txt" | grep -v "*.fq"`
    do
        echo "${j} > `basename ${j} .txt`.fq"
        python format_reads.py -i ${j} -n ${i} -q "h" > `basename ${j} .txt`.fq
    done
done


