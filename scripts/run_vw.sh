vw=../
vg=../

model=$1

gam=$2

cat $gam  | ${vw} -t -i $model -p /dev/stdout
