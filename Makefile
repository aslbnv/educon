VENV = venv
PYTHON = $(VENV)/bin/python3

venv: clean
	python3 -m venv $(VENV)

clean: 
	rm -rf $(VENV)