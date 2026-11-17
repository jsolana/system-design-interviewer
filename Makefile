PRACTICE := practice
VENV := $(PRACTICE)/.venv
PY := $(VENV)/bin/python

.PHONY: help practice install env clean

help:
	@echo "make practice   Install dependencies if needed and start the practice app (http://127.0.0.1:7860)"
	@echo "make install    Create practice/.venv and install requirements"
	@echo "make env        Create .env from .env.example if it does not exist"
	@echo "make clean      Remove practice/.venv"

practice: install env
	cd $(PRACTICE) && .venv/bin/python app.py

install: $(VENV)/.installed

$(VENV)/.installed: $(PRACTICE)/requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -q -r $(PRACTICE)/requirements.txt
	touch $@

env:
	@test -f .env || (cp .env.example .env && echo "Created .env: set OPENAI_BASE_URL, OPENAI_API_KEY and OPENAI_MODEL before using the app")

clean:
	rm -rf $(VENV)
