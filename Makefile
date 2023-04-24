up:
	docker compose -f docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down

rebuild:
	docker compose -f docker-compose-local.yaml down
	docker compose -f docker-compose-local.yaml build
	docker compose -f docker-compose-local.yaml up -d
test:
	pytest -v -s tests/