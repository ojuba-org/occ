#! /bin/bash
xgettext -o "po/occ.pot" -L python *.py mechanisms/*.py Plugins/*.py OjubaControlCenter/*.py
pushd po
for i in *.po
do
po=$i
msgmerge "$po" "occ.pot" > "$po.tmp" && \
mv "$po.tmp" "$po"
done
popd
