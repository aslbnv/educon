run:
	python education_portal/manage.py runserver

tasks:
	python education_portal/manage.py process_tasks

makemigrations:
	python education_portal/manage.py makemigrations

migrate:
	python education_portal/manage.py migrate