.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  ref		Reformat code"
	@echo "  run		Start the app"
	@echo "  docker		Docker container build"
	@echo "  migrate	Alembic migrate database"
	@echo "  generate	Alembic generate database"
	@echo "  req		pyproject.toml >> requirements.txt"

.PHONY:	blue
blue:
	poetry run blue app/

.PHONY: isort
isort:
	poetry run isort app/

.PHONY: ruff
ruff:
	poetry run ruff check app/ --fix --respect-gitignore

.PHONY: ref
ref: blue isort ruff

.PHONY: run
run:
	poetry run fastapi dev app

.PHONY: docker
docker:
	docker-compose up -d

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

.PHONY: generate
generate:
	poetry run alembic revision --autogenerate

.PHONY: req
req:
	@poetry export --without-hashes --without-urls | sed 's/;.*//' | tee requirements.txt
