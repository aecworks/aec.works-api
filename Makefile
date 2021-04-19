.PHONY: tests setup env

start:
	docker network create aecworks-network || true
	docker-compose up -d redis postgres

serve:
	export CELERY_TASK_ALWAYS_EAGER=1
	export DJANGO_DEBUG=1
	bash ./scripts/serve-dev.sh

stop:
	docker-compose down

bash:
	docker exec -it django bash

attach:
	docker attach django

logs:
	docker logs django -f

rebuild:
	docker-compose build --force-rm
	make start

lint:
	bash ./scripts/lint.sh

format:
	bash ./scripts/format.sh

test:
	bash ./scripts/test.sh

coverage:
	bash ./scripts/coverage.sh

clean:
	bash ./scripts/clean.sh

setup:
	bash ./scripts/setup.sh
	make env

env:
	bash ./scripts/envup.sh

seed:
	bash ./scripts/seed.sh
