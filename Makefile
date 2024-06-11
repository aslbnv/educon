VENV = venv

venv: clean
	python3 -m venv $(VENV)

clean: 
	rm -rf $(VENV)