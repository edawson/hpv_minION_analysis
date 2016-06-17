BIN_DIR=bin
MODEL_DIR=models
CWD:=$(shell pwd)

all: $(BIN_DIR)/vw $(BIN_DIR)/vg $(BIN_DIR)/mash

$(BIN_DIR)/vw: .pre-build
	ln -s `pwd`/vw-8.20151121 `pwd`/$(BIN_DIR)/vw

$(BIN_DIR)/vg: ./vg/bin/vg .pre-build
	ln -s `pwd`/vg/bin/vg `pwd`/$(BIN_DIR)/vg

./vg/bin/vg:
	cd ./vg && $(MAKE) -j 4 static

$(BIN_DIR)/mash: .pre-build $(BIN_DIR)/bin/capnp
	cd Mash && ./bootstrap.sh && ./configure --prefix=`pwd`/Mash --with-capnp=$(CWD)/bin && make && make install && cd .. && ln -s `pwd`/Mash/mash `pwd`/bin/mash

.pre-build:
	mkdir $(BIN_DIR) && touch .pre-build

$(BIN_DIR)/bin/capnp: .pre-build
	tar zxf capnproto-c++-0.5.3.tar.gz
	cd capnproto-c++-0.5.3 && ./configure --prefix=$(CWD)/bin && make -j6 check && make install

.edit_paths:

.PHONY: clean clobber install

clean:
	rm .pre-build
	rm $(BIN_DIR)
	rm $(MODEL_DIR)
