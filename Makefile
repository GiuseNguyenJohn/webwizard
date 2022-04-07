.PHONY: run clean

VENV = webwizard_venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run_tests:
	python3 -m unittest discover .

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
