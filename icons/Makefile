
ECHO := echo
RM := $(shell which rm | egrep '/' | sed  's/\s//g')

all:
	@$(ECHO) "*** Converting: icons..."
	@sh ./mkicons.sh

clean:
	@$(ECHO) "*** Cleaning icons..."
	@$(RM) -f *.png
	
