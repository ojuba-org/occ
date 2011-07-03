DESTDIR?=/
datadir?=$(DESTDIR)/usr/share
INSTALL=install

SOURCES=$(wildcard *.desktop.in)
TARGETS=${SOURCES:.in=}

POTFILE=$(shell cat po/POTFILES.in.in)
POSOURCES=$(foreach i, $(POTFILE), $(wildcard $(i) ))

all: $(TARGETS)

po/POTFILES.in: po/POTFILES.in.in
	echo "" >po/POTFILES.in
	for i in $(POSOURCES); do \
	echo $${i} >>po/POTFILES.in; \
	done

pos: po/POTFILES.in
	make -C po all

install: all
	python setup.py install -O2 --root $(DESTDIR)

%.desktop: %.desktop.in pos
	intltool-merge -d po $< $@

clean:
	rm -f $(TARGETS)

