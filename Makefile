.PHONY: run test lint fmt precommit docker

run:
	uvicorn app.main:app --reload

test:
	pytest -q

lint:
	ruff check .

fmt:
	black .
	ruff check --fix .

precommit:
	pre-commit install

docker:
	docker build -t notes-api . && docker run -p 8000:8000 -e SECRET_KEY=dev notes-api
