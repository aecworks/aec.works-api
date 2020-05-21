.PHONY: tests

docker-start:
	docker network create aecworks-network || true
	docker-compose up -d web

docker-db:
	docker network create aecworks-network || true
	docker-compose up -d db

docker-bash:
	docker exec -it django bash

docker-logs:
	docker logs django -f

docker-rebuild:
	docker-compose build --force-rm
	make start

seed:
	python manage.py loaddata api/aecworks/fixtures/users.json
	python manage.py seed

dev:
	DJANGO_DEBUG=1 python manage.py runserver

test:
	python manage.py test api/community/tests

clean:
	python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python3 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

