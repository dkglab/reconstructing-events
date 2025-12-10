SHELL := /usr/bin/env bash

EYE := ./tools/eye/bin/eye
RIOT := ./tools/jena/bin/riot
ARQ := ./tools/jena/bin/arq
SHACL := ./tools/jena/bin/shacl

RULES := $(wildcard rules/*.n3)
RPO_RULES := $(wildcard rules/rpo/*.n3)

define green
\033[0;32m$(1)\033[0m
endef

define red
\033[0;31m$(1)\033[0m
endef

define log
	@echo -e "\\n$(call green,$(1))"
endef

define validate
	$(call log,Validating $(1) using $(2))
	@echo $(SHACL) validate --data $(1) --shapes $(2) --text
	@output=$$($(SHACL) validate --data $(1) --shapes $(2) --text) ; \
	[ "$$output" == "Conforms" ] && \
	{ echo -e "$(call green,Valid!)" ; } || \
	{ echo -e "\\n$$output\\n\\n$(call red,SHACL validation failed with $(2); see errors above)" ; exit 1 ; }
endef

EMPTY :=
SPACE := $(EMPTY) $(EMPTY)
join-with = $(subst $(SPACE),$1,$(strip $2))
tooldir = $(call join-with,/,$(wordlist 1,2,$(subst /, ,$1)))

.PHONY: clean superclean

clean:
	rm -f tools/import-triples/triples.ttl triples.ttl triples-inferred.ttl events.ttl

superclean: clean
	@$(MAKE) -s -C tools/eye clean
	@$(MAKE) -s -C tools/jena clean
	@$(MAKE) -s -C tools/import-triples clean

$(EYE) $(RIOT) $(ARQ):
	$(MAKE) -C $(call tooldir,$@)

tools/import-triples/triples.ttl:
	$(MAKE) -C tools/import-triples

triples.ttl: tools/import-triples/triples.ttl | $(RIOT)
	$(RIOT) --formatted=ttl --set ttl:indentStyle=long $< > $@

ecrm/object-properties.ttl: ecrm/ecrm.ttl queries/object-properties.rq | $(ARQ)
	$(ARQ) --data $< --query $(word 2,$^) --results TTL > $@

ecrm/datatype-properties.ttl: ecrm/ecrm.ttl queries/datatype-properties.rq | $(ARQ)
	$(ARQ) --data $< --query $(word 2,$^) --results TTL > $@

triples-inferred.ttl: triples.ttl ecrm/object-properties.ttl ecrm/datatype-properties.ttl $(RULES) $(RPO_RULES) | $(EYE) $(RIOT)
	$(EYE) \
	--quiet \
	--nope \
	--turtle $< \
	--turtle ecrm/object-properties.ttl \
	--turtle ecrm/datatype-properties.ttl \
	$(RULES) \
	$(RPO_RULES) \
	--pass \
	> unformatted-$@
	$(RIOT) --formatted=ttl --set ttl:indentStyle=long prefixes.ttl unformatted-$@ > $@

events.ttl: triples-inferred.ttl shapes/events.ttl queries/events.rq | $(ARQ) $(SHACL)
	$(call validate,$<,$(word 2,$^))
	$(ARQ) --data $< --query $(word 3,$^) --results TTL > $@
