build:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

run:
	make build
	docker compose up
