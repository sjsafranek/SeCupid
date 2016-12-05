##=======================================================================##
## Makefile
## Created: Wed Aug 05 14:35:14 PDT 2015 @941 /Internet Time/
# :mode=makefile:tabSize=3:indentSize=3:
## Purpose: 
##======================================================================##

.PHONY: init install test

init:
    pip3 install -r requirements.txt

install:
	python3 setup.py install

test:
    py.test tests
