.PHONY: run clean

VENV = webwizard_venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run:
	sudo apt install python3.9

$(VENV)/bin/activate: requirements.txt
	python3.9 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run_tests:
	python3 -m unittest discover .

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
