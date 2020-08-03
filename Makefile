.PHONY: tests

docker-start:
	docker network create aecworks-network || true
	docker-compose up -d web

docker-db:
	docker network create aecworks-network || true
	docker-compose up -d postgres

docker-bash:
	docker exec -it django bash

docker-attach:
	docker attach django

docker-logs:
	docker logs django -f

docker-rebuild:
	docker-compose build --force-rm
	make docker-start

seed:
	python manage.py seed

dev:
	DJANGO_DEBUG=1 python manage.py runserver

lint:
	bash ./scripts/lint.sh

test:
	python -m pytest

clean:
	python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python3 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

setup:
	bash ./scripts/setup.sh

