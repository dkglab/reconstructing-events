PYTHON := ./venv/bin/python
PIP := ./venv/bin/python -m pip

.PHONY: all clean

all: triples.ttl

clean:
	rm -rf venv triples.ttl

$(PYTHON):
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

triples.ttl: import-triples.py | $(PYTHON)
	$(PYTHON) $< $@
