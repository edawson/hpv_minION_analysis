SHELL=bash
VG:=

run: hpv_16_reads.fq HPV_pan.sketch.msh HPV16_type_msh_pred.txt HPV16_subtype_msh_pred.txt minIONs_pred.txt

hpv_16_reads.fq:
	if [ ! -e ./ref ]; then ln -s ../3_HPV_PanGenome/ref/ ./ref; fi
	if [ ! -e hpv_16.fa ]; then ln -s ../1_basic_pred_model/hpv_16.fa .; fi
	../scripts/make_reads.sh ./hpv_16.fa && mv n1000.e0.05.i0.10.l7500.reads.hpv_16.fq  hpv_16_reads.fq 

hpv_minION_reads.fastq:
	if [ ! -e ./hpv_minION_reads.fastq ]; then ln -s ../minION_data/hpv_minION_reads.fastq . ; fi

HPV_pan.sketch.msh:
	../bin/mash sketch -s 1000 -k 21 -o $@ ref/*.fa*

HPV_16.sketch.msh:
	if [ ! -d hpv16 ]; then mkdir hpv16; fi && cp ../3_HPV_PanGenome/variant/Human16_* hpv16/ && cp ../3_HPV_PanGenome/ref/Human16_* hpv16/
	for i in `ls ../3_HPV_PanGenome/ref/ | grep -v "Human16_" | grep -v "fastqs" | head -n 5`; do cp ../3_HPV_PanGenome/ref/$$i hpv16/ ;done
	../bin/mash sketch -s 7000 -k 21 -o $@ hpv16/*


HPV16_type_msh_pred.txt: HPV_pan.sketch.msh
	../bin/mash dist -r $< hpv_16_reads.fq | sort -n -k3 | head -n 20 | tee $@

HPV16_subtype_msh_pred.txt: HPV_16.sketch.msh
	../bin/mash dist $< hpv_16_reads.fq | sort -n -k3 | head -n 20 | tee $@


HPV_pan.sketch10000_k18.msh:
	for i in 8 10 15 18 ; do \
		for j in 1000 3000 7000 10000 ; do ../bin/mash sketch -s $$j -k $$i -o HPV_pan.sketch$${j}_k$${i}.msh ref/*.fa* ; done ; done

minIONs_type_s10000_k18_pred.txt: HPV_pan.sketch10000_k18.msh hpv_minION_reads.fastq
	for i in 8 10 15 18 ; do \
		for j in 1000 3000 7000 10000 ; do echo "Sketch size: $${j} and Kmer size: $${i}"; echo ""; ../bin/mash dist -r  HPV_pan.sketch$${j}_k$${i}.msh hpv_minION_reads.fastq | sort -n -k3 | head -n 5 | tee minIONs_type_s$${j}_k$${i}_pred.txt ; echo "" ; done ; done

minIONs_type_s10000_k18_m40_pred.txt: HPV_pan.sketch10000_k18.msh hpv_minION_reads.fastq
	for i in 1 2 10 20 40 100; do echo "Minimum kmer occurence: $${i}"; echo ""; ../bin/mash dist -r -m $$i $< hpv_minION_reads.fastq | sort -n -k3 | head -n 5 | tee minIONs_type_s10000_k18_m$$i_pred.txt ; echo "" ; done

minIONs_subtype_s10000_k18_m40_pred.txt: HPV_16.sketch.msh hpv_minION_reads.fastq 
	for i in 1 2 10 20 40 100; do echo "Minimum kmer occurence: $${i}"; echo ""; ../bin/mash dist -r -m $$i $< hpv_minION_reads.fastq | sort -n -k3 | head -n 5 | tee minIONs_subtype_s10000_k18_m$$i_pred.txt ; echo "" ; done

hpv_subtype_s10000_k18_m40_pred.txt: HPV_16.sketch.msh hpv_16_reads.fq
	for i in 1 2 10 20 40 100; do echo "Minimum kmer occurence: $${i}"; echo ""; ../bin/mash dist -r -m $$i $< hpv_16_reads.fq | sort -n -k3 | head -n 5 | tee hpv_subtype_s10000_k18_m$$i_pred.txt ; echo "" ; done

minIONs_type_pred.txt: HPV_pan.sketch.msh hpv_minION_reads.fastq
	../bin/mash dist -r $< hpv_minION_reads.fastq | sort -n -k3 | head -n 20 | tee $@

minIONs_subtype_pred.txt: HPV_16.sketch.msh hpv_minION_reads.fastq
	../bin/mash dist -r -m 20 $< hpv_minION_reads.fastq | sort -n -k3 | head -n 20 | tee $@

minIONs_individualReads_subtype_pred.txt: HPV_16.sketch.msh hpv_minION_reads.fastq hpv_16_reads.fq
	../bin/mash dist -i $< hpv_minION_reads.fastq | sort -n -k3 | head -n 20 | tee $@
	echo "Comparing to null (HPV simmed reads): "
	../bin/mash dist -i $< hpv_16_reads.fq | sort -n -k3 | head -n 20 | tee hpv_16_ind_pred.txt

.PHONY: run clean clobber

clean:
	$(RM) *.msh
	$(RM) hpv_16/
	$(RM) *pred.txt

clobber:
	$(RM) *.fq
