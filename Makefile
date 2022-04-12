.PHONY: run clean

run:
	sudo apt install python3

setup: requirements.txt
	pip3 install -r requirements.txt

run_tests:
	python3 -m unittest discover .

clean:
	rm -rf __pycache__
