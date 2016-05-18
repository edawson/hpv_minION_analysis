
CWD=`pwd`
for i in scripts/*
do
    sed -e 's/mash=.*$/mash=${CWD}/Mash/mash/' scripts/$i
done
