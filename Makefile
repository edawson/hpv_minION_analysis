BIN_DIR=bin
MODEL_DIR=models


all: $(BIN_DIR)/vw $(BIN_DIR)/vg $(BIN_DIR)/mash

$(BIN_DIR)/vw: .pre-build
	ln -s `pwd`/vw-8.20151121 `pwd`/$(BIN_DIR)/vw

$(BIN_DIR)/vg: ./vg/bin/vg .ppre-build
	ln -s `pwd`/vg/bin/vg `pwd`/$(BIN_DIR)/vg

./vg/bin/vg:
	cd ./vg && $(MAKE) -j 4 static

$(BIN_DIR)/mash: .pre-build
	cd Mash && ./bootstrap.sh && ./configure --prefix=`pwd`/Mash && make && make install && cd .. && ln -s `pwd`/Mash/mash `pwd`/bin/mash

.pre-build:
	mkdir $(BIN_DIR) && touch .pre-build

.edit_paths:

.PHONY: clean clobber install

clean:
	rm .pre-build
	rm $(BIN_DIR)
	rm $(MODEL_DIR)
