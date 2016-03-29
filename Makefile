VG_DIR=./vg_main
VG=${VG_DIR}/bin/vg
ref_base="linear"

.PHONY: analysis clean map index vectorize cluster plot construct


analysis: vg map index vectorize cluster plot construct circularize circular

vg:
	cd $(VG_DIR) && make -j 4 static && cd .. && cp ${VG_DIR}/bin/vg ./vg

map: vg
	${VG} map -x ${ref_base}.xg -g ${ref_base}.gcsa 

construct: vg
	${VG} construct -r hpv16.ref.fa -v hpv_16_manual.vcf.gz > ${ref_base}.vg
	#${VG} view -F -v ${ref_base}.gfa > ${ref_base}.vg

index: construct vg
	${VG} index -x ${ref_base}.xg -g ${ref_base}.gcsa -k 15 ${ref_base}.vg

vectorize: index map vg
	${VG} vectorize -x ${ref_base}.xg ${ref_base}.gam > ${ref_base}.vectors.txt

cluster: vectorize index map vg

plot: cluster vectorize index map vg
