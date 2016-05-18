SHELL=bash
VG:=../vg/bin/vg
WABBIT:=../bin/vw

fasta_file:=hpv16.ref.fasta
vcf_file:=hpv16_vcf_replacedINDELS_coord.vcf.gz
base_name:=hpv16_manIND






run: trained.model test_pred.txt $(base_name).circ.vg train_me.fq train_me.vecs.wabbit

$(base_name).circ.xg: $(base_name).circ.vg
$(base_name).circ.vg:
	$(VG) construct -r $(fasta_file) -v $(vcf_file) -m 50 > $(base_name).vg
	$(VG) circularize -p HPV16Ref $(base_name).vg > $(base_name).circ.vg
	$(VG) index -x $(base_name).circ.xg -g $(base_name).circ.gcsa -k 16 $(base_name).circ.vg

train_me.fq:
	if [-e jobfile.txt ]; then $(RM) jobfile.txt; fi
	echo "../scripts/make_reads.sh hpv_1.fa" >> jobfile.txt
	echo "../scripts/make_reads.sh hpv_2.fa" >> jobfile.txt
	echo "../scripts/make_reads.sh hpv_16.fa" >> jobfile.txt
	python ../LaunChair/launcher.py -i jobfile.txt -c 1 && $(RM) jobfile.txt
	cat n*.fq | ../scripts/remove_numbers.sh | ../scripts/shuf.py > $@

train_me.gam: train_me.fq $(base_name).circ.vg
	$(VG) map -t 4 -B 128 -GX .6 -A 2 -x $(base_name).circ.xg -g $(base_name).circ.gcsa -f $< > $@

train_me.vecs.wabbit: train_me.gam train_me.fq $(base_name).circ.xg
	$(VG) vectorize -w -a -x $(base_name).circ.xg -M mappings.text $< > $@
	
trained.model: train_me.vecs.wabbit train_me.fq train_me.gam $(base_name).circ.xg
	if [-e .cache ]; then rm .cache; fi  && head -n 300 $< | $(WABBIT) --oaa 3 --binary --ngram 5 --passes=20 --threads  -f trained.model --cache_file .cache

test_pred.txt: trained.model train_me.vecs.wabbit train_me.fq train_me.gam $(base_name).circ.xg
	if [  -e .cache ]; then rm .cache; fi && cat train_me.vecs.wabbit | $(WABBIT) -i trained.model -p /dev/stdout | tee $@ | python ../scripts/make_confusion_matrix.py -c mappings.text

.PHONY: run clean clobber

clean:
	$(RM) trained.model
	$(RM) .cache

clobber: clean
	$(RM) *.reads.txt
	$(RM) *reads*fq
	$(RM) *.fai
	$(RM) *.vg
	$(RM) *.gcsa
	$(RM) *.lcp
	$(RM) *.xg
	$(RM) *.gam
	$(RM) *.fq
	$(RM) jobfile.txt

