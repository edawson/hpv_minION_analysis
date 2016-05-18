indir=$1
jobfile=${indir}.jobfile.txt
for i in `ls $indir | grep ".fa$\|.fasta$"`
do
    echo "~/hpv_minION_analysis/scripts/make_reads.sh $i" >> $jobfile
done

python ../LaunChair/launcher.py -i $jobfile -c 1
