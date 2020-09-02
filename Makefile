.PHONY: tests

start:
	docker network create aecworks-network || true
	docker-compose up -d web

db:
	docker network create aecworks-network || true
	docker-compose up -d postgres

bash:
	docker exec -it django bash

attach:
	docker attach django

logs:
	docker logs django -f

rebuild:
	docker-compose build --force-rm
	make start

seed:
	python manage.py seed

dev:
	CELERY_TASK_ALWAYS_EAGER=1 DJANGO_DEBUG=1 python manage.py runserver

lint:
	bash ./scripts/lint.sh

format:
	bash ./scripts/format.sh

test:
	python -m pytest

clean:
	python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python3 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

setup:
	bash ./scripts/setup.sh

worker:
	celery -A api worker -l info
