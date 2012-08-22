# Makefile for Mupy
#

tag = $(shell git describe --abbrev=0)
ver = $(shell git describe --abbrev=0 | egrep -o '([0-9]+\.){1,10}[0-9]+' | sed -e 's/\./_/g')
name   	   = $(shell basename $(shell pwd))

.PHONY: dist

	
dist:
	git archive --format tar --prefix $(name)-$(ver)/ -o $(name)-$(ver).tar $(tag)
	gzip -f $(name)-$(ver).tar



