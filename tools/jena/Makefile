SHELL := /usr/bin/env bash
.SHELLFLAGS := -O extglob -c

TOOLS := curl tar

X := $(foreach tool,$(TOOLS),\
	$(if $(shell which $(tool)),,\
	$(error Please install $(tool) and ensure it is in your path)))

JENA_HOST := https://dlcdn.apache.org/jena/binaries
JENA_VERSION := 5.6.0

.PHONY: all clean

all: bin/riot

clean:
	rm -rf !(Makefile)

bin/riot:
	curl -L $(JENA_HOST)/apache-jena-$(JENA_VERSION).tar.gz \
	| tar -zxf - --strip-components 1
