for i in $(ls *.svg | sed 's/ /___/g' | sed 's/\.svg/ /g'); do
    fn=$(echo $i | sed 's/___/ /g')
	convert -background none "${fn}.svg" -resize 64x64 "${fn}.png"
done
