
ECHO := echo
RM := $(shell which rm | egrep '/' | sed  's/\s//g')

all:
	@$(ECHO) "*** Converting: icons..."
	@for i in $(shell ls *.svg|sed -e 's/ /\\ /g' -e 's/\.svg//g' ); do \
		convert -background none "$${i}.svg" -resize 64x64 "$${i}.png"; \
	done

clean:
	@$(ECHO) "*** Cleaning icons..."
	@$(RM) -f *.png
	
