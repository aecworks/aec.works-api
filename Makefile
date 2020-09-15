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
	docker exec -it django python manage.py seed

local:
	CELERY_TASK_ALWAYS_EAGER=1 DJANGO_DEBUG=1 python manage.py runserver

lint:
	docker exec django bash ./scripts/lint.sh

format:
	docker exec django bash ./scripts/format.sh

test:
	docker exec django python -m pytest

clean:
	python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

setup:
	bash ./scripts/setup.sh
