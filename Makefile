.PHONY: test

bash:
	docker exec -it django bash

seed:
	python manage.py loaddata api/aecguide/fixtures/users.json
	python manage.py seed_companies

dev:
	DJANGO_DEBUG=1 python manage.py runserver

start:
	docker network create aecguide-network || true
	docker-compose up -d db

logs:
	docker logs django -f

rebuild:
	docker-compose build --force-rm
	make start


clean:
	python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python3 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

