PYTHON ?= python3
VENV_PYTHON := .venv/bin/python
VENV_PIP := .venv/bin/pip

.PHONY: setup migrate dev-backend dev-frontend test catalogue-check frontend-build check

setup:
	$(PYTHON) -m venv .venv
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r backend/requirements.txt
	npm --prefix frontend install

migrate:
	$(VENV_PYTHON) backend/manage.py migrate

dev-backend:
	$(VENV_PYTHON) backend/manage.py runserver 0.0.0.0:8000

dev-frontend:
	npm --prefix frontend run dev

test:
	$(VENV_PYTHON) backend/manage.py test core

catalogue-check:
	$(VENV_PYTHON) backend/manage.py check_catalogue

frontend-build:
	npm --prefix frontend run build

check: test catalogue-check frontend-build
