VENV = venv
ACTIVATE = .\$(VENV)\Scripts\activate

run:
	$(ACTIVATE) && python education_portal/manage.py runserver