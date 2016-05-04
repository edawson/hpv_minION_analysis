mash=../../../Mash/mash

for i in `ls | grep "fa" | grep "Human"`
do
    $mash sketch -k 18 -s 5000 $i
done
$mash paste hpv_pan16 *.msh


