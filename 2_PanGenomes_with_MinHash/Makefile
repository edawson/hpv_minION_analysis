SHELL=bash
VG:=

run: hpv_16_reads.fq HPV_pan.sketch.msh HPV16_type_msh_pred.txt HPV16_subtype_msh_pred.txt minions_pred.txt

hpv_16_reads.fq:
	if [ -ne ./ref ]; then ln -s ../3_HPV_PanGenome/ref/ ./ref; fi
	if [ -ne hpv_minion_reads.fq ]; then ln -s ../minion_data/hpv_minION_reads.fastq .; fi
	if [ -ne hpv_16.fa ]; then ln -s ../1_basic_pred_model/hpv_16.fa .; fi
	../scripts/make_reads.sh ./hpv_16.fa && mv n1000.e0.05.i0.10.l7500.reads.hpv_16.fq  hpv_16_reads.fq 

HPV_pan.sketch.msh:
	../bin/mash sketch -s 7000 -k 21 -o $@ ref/*.fa*

HPV16_type_msh_pred.txt: HPV_pan.sketch.msh
	../bin/mash dist -r $< hpv_16_reads.fq | tee $@

HPV_16.sketch.msh:
	mkdir hpv16 && cp ../3_HPV_PanGenome/variant/Human16_* hpv16/
	../bin/mash sketch -o HPV_16.sketch.msh hpv16/*

HPV16_subtype_msh_pred.txt: HPV_16.sketch.msh
		../bin/mash dist $< test_data/hpv_16_reads.fq

minions_pred.txt: HPV_pan.sketch.msh HPV_16.sketch.msh test_data

.PHONY: run clean clobber

clean:

clobber:
