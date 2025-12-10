SHELL := /usr/bin/env bash
.SHELLFLAGS := -O extglob -c

TOOLS := curl tar

X := $(foreach tool,$(TOOLS),\
	$(if $(shell which $(tool)),,\
	$(error Please install $(tool) and ensure it is in your path)))

EYE_HOST := https://github.com/eyereasoner/eye/archive
EYE_VERSION := refs/tags/v11.23.2

.PHONY: all clean

all: eye

clean:
	rm -rf !(Makefile) .gitignore .github

eye:
	curl -L $(EYE_HOST)/$(EYE_VERSION).tar.gz \
	| tar zxvf - --strip-components 1
	./install.sh --prefix=$(CURDIR)
