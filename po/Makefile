POTFILE=$(shell cat POTFILES.in)
SOURCES=$(addprefix ../, $(POTFILE))
POFILES=$(wildcard *.po)
MOFILES=$(patsubst %.po,%.mo,$(POFILES))

all: occ.pot $(MOFILES)

occ.pot: $(SOURCES)
	echo $(SOURCES)
	intltool-update -g occ -p

%.mo: %.po
	msgfmt $*.po -o $*.mo
	mkdir -p ../locale/$*/LC_MESSAGES/ || :
	cp $*.mo ../locale/$*/LC_MESSAGES/occ.mo

%.po: occ.pot
	intltool-update -g occ -d $*

