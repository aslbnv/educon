VENV = venv
ACTIVATE = .\$(VENV)\Scripts\activate

run:
	$(ACTIVATE) && python education_portal/manage.py runserver

tasks:
	$(ACTIVATE) && python education_portal/manage.py process_tasks